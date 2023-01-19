import copy
import os

import cplex

from structures.graph.generate_network import generate_network
from structures.scheduling.schedule import Schedule


# arcs, source_node, sink_node, job_processing_sum, closed_timeslots

def solve_maxflow_cplex_with_reopt(instance, solver_type: str):
    # 0. Note: Important to deep copy input to avoid modifying problem instance.
    time_horizon = copy.deepcopy(instance.time_horizon)
    jobs = copy.deepcopy(instance.jobs)

    # 1. Find initial solution.
    network = generate_network(time_horizon.time_slots, jobs)
    total_sum = sum(job.processing_time for job in jobs)

    # for arc in arcs:
    #     print(arc.source_node.value, arc.terminal_node.value, arc.capacity)
    # Create cplex Model and specify properties
    model = cplex.Cplex()
    model.set_problem_name("Max Flow model")
    # model.set_problem_type(cplex.Cplex.problem_type.LP)
    model.parameters.lpmethod.set(model.parameters.lpmethod.values.network)
    # Disable logging when measuring time.
    model.set_log_stream(None)
    model.set_error_stream(None)
    model.set_warning_stream(None)
    model.set_results_stream(None)

    # Parameter: add the different arcs
    names = []
    names_by_term_map = {}
    for arc in network.arcs:
        names.append(f"{arc.source_node.value}#{arc.terminal_node.value}")
        names_by_term_map
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
    upr_bnd = []
    for arc in network.arcs:
        upr_bnd.append(arc.capacity)

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

        # print([arc_names, arc_c])
        constraints.append([arc_names, arc_c])

    # Give unique name for each constraint.
    constraint_names = ["c" + str(i) for i, _ in enumerate(constraints)]

    # Add right hand side for each conservation of flow constraint.
    # 1.0 * <inflow_arc> + (-1.0) * <outflow_arc> == 0
    rhs = [0] * len(constraints)

    # Add sense for each conservation of flow constraint (=, denoted "E" for equality).
    constraint_senses = ["E"] * len(constraints)

    # And add the constraints to the model.
    model.linear_constraints.add(names=constraint_names,
                                 lin_expr=constraints,
                                 senses=constraint_senses,
                                 rhs=rhs)
    # Solve the problem
    # print("Problem Type: %s" % model.problem_type[model.get_problem_type()])
    model.solve()
    # sol = (model.solution.get_values())

    # print(model.solution.get_values())
    # print("Objective", model.solution.get_objective_value(), job_processing_sum)

    if model.solution.get_objective_value() == total_sum:
        # print("Objective", model.solution.get_objective_value(), job_processing_sum)
        job_to_timeslot_mapping = []
        # model.write("prob.lp")

        for variable, value in zip(model.variables.get_names(), model.solution.get_values()):
            # print(variable, value)
            arc_info = variable.split("#")

            source_node_info: list = arc_info[0].split("_")  # As we care only about job and timeslot nodes
            dest_node_info: list = arc_info[1].split("_")  # [0] - node type (job or timeslot), [1] (node number)
            if source_node_info[0] == "j" and dest_node_info[0] == "t":
                if value == 1:  # we care only where the arc flow is 1
                    # Schedule job j at timeslot t
                    job_to_timeslot_mapping.append((f"Job_{source_node_info[1]}", f"Slot_{dest_node_info[1]}"))

        initial_schedule = Schedule(True, job_to_timeslot_mapping)

        closed_timeslots = []
        # 2. Attempt to find a better solution.
        for timeslot in time_horizon.time_slots:
            # 2.1. Close timeslot.
            timeslot.is_open = False
            closed_timeslots.append(f"t_{timeslot.start_time}")
            # 2.2. Check for feasible solution in the other timeslots
            total_sum = sum(job.processing_time for job in jobs)

            # Flow values is used to pass the assigned flow values from previous computations.
            for closed_timeslot in closed_timeslots:

                model.variables.set_upper_bounds()

            # initial_bounds = flow_bounds
            # print(schedule.is_feasible)
            if schedule.is_feasible:
                # 2.3. If a better solution is found update the initial schedule.
                initial_schedule = schedule
            else:
                # 2.4. If no better solution is found open the time slot again and continue.
                timeslot.is_open = True
                closed_timeslots.remove(f"t_{timeslot.start_time}")
    else:
        # If no feasible schedule can be found return.
        return Schedule(False, [])
