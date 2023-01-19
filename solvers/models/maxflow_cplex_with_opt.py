import os

import cplex

from structures.scheduling.schedule import Schedule


def solve_maxflow_cplex_with_opt(arcs, source_node, sink_node, job_processing_sum):
    # Create cplex Model and specify properties
    model = cplex.Cplex()
    # Disable logging when measuring time.
    model.set_log_stream(None)
    model.set_error_stream(None)
    model.set_warning_stream(None)
    model.set_results_stream(None)

    model.set_problem_name("Max Flow model")
    if os.path.isfile("lpex.bas"):
        model.start.read_basis("lpex.bas")
    if os.path.isfile("model.sol"):
        model.start.read_start("model.sol")


    model.set_problem_type(cplex.Cplex.problem_type.LP)
    # model.parameters.lpmethod.set(model.parameters.lpmethod.values.network)




    # Parameter: add the different arcs
    names = [f"n{arc.source_node.value}n{arc.terminal_node.value}" for arc in arcs]

    # Objective: Maximise the flow in the sink node.
    w_obj = []
    for arc in arcs:
       # print(arc.source_node.value, arc.terminal_node.value)
        if arc.terminal_node == sink_node:
            w_obj.append(1.0)
        else:
            w_obj.append(0.0)

    # Constraint: Ensure the flow through each arc is less than or equal to its capacity and greater or equal to 0.
    # (e.g) 0 (lower_bound) <= flow through each arc <= arc capacity (upper bound)
    low_bnd = [0.0 for arc in arcs]

    upr_bnd = []
    for arc in arcs:
        # if f"n{arc.source_node.value}n{arc.terminal_node.value}" in arc_bounds:
        #     #print(arc_bounds[f"{arc.source_node.value}#{arc.terminal_node.value}"])
        #     upr_bnd.append(arc_bounds[f"n{arc.source_node.value}n{arc.terminal_node.value}"])
        # else:
        upr_bnd.append(arc.capacity)

    # Set sense for the objective
    model.objective.set_sense(model.objective.sense.maximize)
    # Add variables, limits and specify objective function.
    model.variables.add(names=names, obj=w_obj, lb=low_bnd, ub=upr_bnd)

    # Constraint: Ensure the inflow of every node equals the outflow of the same node.
    constraints = []
    visited_arcs = []
    for arc in arcs:

        n1 = arc.source_node
        n2 = arc.terminal_node

        # # Check if node has been visited. If it has, skip it
        # # otherwise we will add a duplicate constraint.
        if n2 in visited_arcs:
            continue

        # Make sure the node is not the source or the sink
        # as constraints for those are covered in the other.
        if n2 == sink_node or n2 == source_node:
            continue

        # Mark node as visited
        visited_arcs.append(n2)

        # Names of the arcs involved in the constraint
        arc_names = []
        arc_c = []

        for arc2 in arcs:
            # Find all arcs where the current terminal node equals the arc's terminal node.
            # Those are the inflow arcs for the current terminal node.
            if arc2.terminal_node == n2:
                arc_names.append(f"n{arc2.source_node.value}n{n2.value}")
                arc_c.append(1.0)
            # Find all arcs where the current terminal node equals the arc's source node.
            # Those are the outflow arcs for the current terminal node.
            if arc2.source_node == n2:
                arc_names.append(f"n{n2.value}n{arc2.terminal_node.value}")
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
    model.solve()
    # print(model.get_time())
    # print(model.variables.get_names())
    # print(model.linear_constraints.get_names())

    if model.solution.get_objective_value() == job_processing_sum:
        job_to_timeslot_mapping = []

        new_bounds = {}
        for variable, value in zip(model.variables.get_names(), model.solution.get_values()):
            # print(variable, value)
            # new_bounds[variable] = value
            arc_info = variable.split("n")

            source_node_info: list = arc_info[1].split("_")  # As we care only about job and timeslot nodes
            dest_node_info: list = arc_info[2].split("_")  # [0] - node type (job or timeslot), [1] (node number)
            if source_node_info[0] == "j" and dest_node_info[0] == "t":
                if value == 1:  # we care only where the arc flow is 1
                    # Schedule job j at timeslot t
                    job_to_timeslot_mapping.append((f"Job_{source_node_info[1]}", f"Slot_{dest_node_info[1]}"))

        model.solution.basis.write("lpex.bas")
        model.solution.write("model.sol")
        return Schedule(True, job_to_timeslot_mapping)
    else:
        return Schedule(False, [])