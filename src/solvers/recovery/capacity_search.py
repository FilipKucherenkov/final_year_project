import copy
import cplex

from problem_classes.graph.generate_network import generate_network
from problem_classes.problem_instances.parsed_instance import ParsedInstance
from problem_classes.scheduling.recovery_schedule import Schedule


def capacity_search(perturbed_instance: ParsedInstance, nominal_solution: Schedule, gamma: int):
    """
    Capacity search method (Max-flow + binary search)
    :param perturbed_instance: ParsedInstance object representing the true scenario.
    :param nominal_solution: Schedule object representing the solution to nominal scenario.
    :param gamma: int value for specifying upper bound on perturbed jobs.
    :return: int value for the minimum required capacity.
    """

    # Note: Important to deep copy input to avoid modifying the problem instance.
    time_horizon = copy.deepcopy(perturbed_instance.time_horizon)
    jobs = copy.deepcopy(perturbed_instance.jobs)

    # Build the corresponding flow network
    network = generate_network(time_horizon.time_slots, jobs)

    # Create cplex Model and specify properties
    model = cplex.Cplex()
    model.set_problem_name("Capacity-Local-Search")
    model.parameters.lpmethod.set(model.parameters.lpmethod.values.network)

    # Disable logging when measuring time.
    model.set_log_stream(None)
    model.set_error_stream(None)
    model.set_warning_stream(None)
    model.set_results_stream(None)

    # Create variable names for the arcs in the network
    names = [f"{arc.source_node.value}#{arc.terminal_node.value}" for arc in network.arcs]

    # Objective: Maximise the flow in the sink node.
    w_obj = []
    for arc in network.arcs:
        if arc.source_node == network.source_node:
            w_obj.append(1.0)
        else:
            w_obj.append(0.0)

    # Constraint: Ensure the flow through each arc is less than or equal to its capacity and greater or equal to 0.
    # (e.g) 0 (lower_bound) <= flow through each arc <= arc capacity (upper bound)
    low_bnd = [0.0 for arc in network.arcs]
    upr_bnd = [arc.capacity for arc in network.arcs]

    # Set sense for the objective
    model.objective.set_sense(model.objective.sense.maximize)

    # Add variables, limits and specify objective function.
    model.variables.add(names=names, obj=w_obj, lb=low_bnd, ub=upr_bnd)

    # Constraint: Ensure the inflow of every node equals the outflow of the same node.
    constraints = []
    visited_arcs = []
    for arc in network.arcs:
        n1 = arc.source_node
        n2 = arc.terminal_node

        # # Check if node has been visited. If it has, skip it
        # # otherwise we will add a duplicate constraint.
        if n1 in visited_arcs:
            continue

        # Make sure the node is not the source or the sink
        # as constraints for those are covered in the other.
        if n1 == network.sink_node or n1 == network.source_node:
            continue

        # Mark node as visited
        visited_arcs.append(n1)

        # Names of the arcs involved in the constraint
        arc_names = []
        arc_c = []

        for arc2 in network.arcs:
            # Find all arcs where the current terminal node equals the arc's terminal node.
            # Those are the inflow arcs for the current terminal node.
            if arc2.terminal_node == n1:
                arc_names.append(f"{arc2.source_node.value}#{n1.value}")
                arc_c.append(1.0)
            # Find all arcs where the current terminal node equals the arc's source node.
            # Those are the outflow arcs for the current terminal node.
            if arc2.source_node == n1:
                arc_names.append(f"{n1.value}#{arc2.terminal_node.value}")
                arc_c.append(-1.0)

        constraints.append([arc_names, arc_c])

    # Give unique name for each constraint in the form c<i> where i is the index of the created constraint.
    constraint_names = ["c" + str(i) for i, _ in enumerate(constraints)]

    # Add right hand side for each conservation of flow constraint.
    # e.g. 1.0 * <inflow_arc> + (-1.0) * <outflow_arc> == 0
    rhs = [0] * len(constraints)

    # Add sense for each conservation of flow constraint (=, denoted "E" for equality).
    constraint_senses = ["E"] * len(constraints)

    # And add the constraints to the model.
    model.linear_constraints.add(names=constraint_names,
                                 lin_expr=constraints,
                                 senses=constraint_senses,
                                 rhs=rhs)
    # Solve the problem
    # model.write("prob.lp")
    model.solve()
    job_processing_sum = sum(job.processing_time for job in perturbed_instance.jobs)

    # ============ Capacity Search =====================#
    last_feasible_bnd = perturbed_instance.number_of_parallel_jobs
    # If solution is not feasible, augment capacity with gamma
    augmented_capacity = gamma + perturbed_instance.number_of_parallel_jobs

    if model.solution.get_status() == 3 or model.solution.get_objective_value() != job_processing_sum:
        sink_arcs = []

        # Change arc upper bound to gamma
        for arc in network.arcs:
            if arc.terminal_node == network.sink_node:
                sink_arcs.append(arc)
                model.variables.set_upper_bounds([(f"{arc.source_node.value}#{arc.terminal_node.value}",
                                                   augmented_capacity)])
        # Solve again with augmented capacity
        model.write("prob.lp")
        model.solve()

        job_processing_sum = sum(job.processing_time for job in perturbed_instance.jobs)
        if model.solution.get_status() != 3 and model.solution.get_objective_value() == job_processing_sum:

            # ===== Binary Search for better capacity ====== #
            lower_bound = 0
            mid = 0
            upper_bound = augmented_capacity

            while lower_bound <= upper_bound:
                mid = (lower_bound + upper_bound) // 2

                for arc in sink_arcs:
                    # Change upper bound
                    model.variables.set_upper_bounds(f"{arc.source_node.value}#{arc.terminal_node.value}", mid)

                model.solve()

                if model.solution.get_objective_value() == job_processing_sum:
                    last_feasible_bnd = mid
                    upper_bound = mid - 1
                else:
                    lower_bound = mid + 1

            # Ensure the found capacity is set as ub
            for arc in sink_arcs:
                model.variables.set_upper_bounds(f"{arc.source_node.value}#{arc.terminal_node.value}",
                                                 last_feasible_bnd)

    return last_feasible_bnd
