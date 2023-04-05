import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from problem_classes.scheduling.recovery_schedule import Schedule
from solvers.recovery.capacity_search import capacity_search


def ip_recovery(perturbed_instance, nominal_solution, v1, v2, gamma):
    """
    IP Recovery Model using Weighted Sum Approach.
    :param perturbed_instance: ParsedInstance object representing the true scenario.
    :param nominal_solution: Schedule object representing the solution to nominal scenario.
    :param v1: float value for first cost coefficient.
    :param v2: float value for second cost coefficient.
    :param gamma: int value for specifying upper bound on perturbed jobs.
    :return: Schedule Object containing the recovered solution.
    """
    # Use capacity search to compute whether augmentation is necessary.
    computed_augmentation = capacity_search(perturbed_instance, nominal_solution, gamma)
    # Create Pyomo model
    model = pyo.ConcreteModel()
    model.name = "IP Recovery Model"

    # Parameter: Set of timeslots.
    model.timeslots = pyo.Set(initialize=perturbed_instance.get_timeslots_lst())
    # Parameter: Set of jobs
    model.jobs = pyo.Set(initialize=perturbed_instance.get_jobs_lst())

    # Parameter: Release times for jobs.
    model.release_times = pyo.Param(model.jobs, within=pyo.NonNegativeIntegers,
                                    initialize=perturbed_instance.get_job_release_times_map())
    # Parameter: Deadlines for jobs.
    model.deadlines = pyo.Param(model.jobs, within=pyo.NonNegativeIntegers,
                                initialize=perturbed_instance.get_job_deadlines_map())
    # Parameter: Processing times for jobs.
    model.processing_times = pyo.Param(model.jobs, within=pyo.NonNegativeIntegers,
                                       initialize=perturbed_instance.get_processing_times_map())

    # Parameter: The allowed number of job units to be scheduled in parallel.
    # Note capacity is augmented using the Gamma parameter.
    model.G = pyo.Param(within=pyo.NonNegativeIntegers, initialize=computed_augmentation) # perturbed_instance.number_of_parallel_jobs + gamma

    # Parameter: Cost coefficient for first cost function.
    model.v1 = pyo.Param(within=pyo.NonNegativeReals, initialize=v1)
    # Parameter: Cost coefficient for second cost function.
    model.v2 = pyo.Param(within=pyo.NonNegativeReals, initialize=v2)

    # Decision variable: Whether slot t is open
    model.y = pyo.Var(model.timeslots, bounds={0, 1}, within=pyo.Binary)
    # Decision variable: Whether any unit of job j is assigned to slot t
    model.x = pyo.Var(model.timeslots, model.jobs, bounds={0, 1}, within=pyo.Binary)

    # Ensure a job is not assigned to a timeslot if that timeslot is not within the job's window
    for t in model.timeslots:
        for j in model.jobs:
            if t < pyo.value(model.release_times[j]) or t >= pyo.value(model.deadlines[j]):
                model.x[t, j].fix(0)

    # Objective function: Minimise the sum of the cost functions subject to the specified weights.
    def objective_rule(model):
        # Cost Function 1: Measures deviation from nominal solution.
        obj1 = sum(sum((model.x[t, j] - nominal_solution.schedule[j][t]) ** 2 for t in model.timeslots) for j in model.jobs)
        # Cost Function 2: Measures the number of active time slots.
        obj2 = sum(model.y[t] for t in model.timeslots)
        return model.v1 * obj1 + model.v2 * obj2
    model.objective = pyo.Objective(rule=objective_rule, sense=pyo.minimize)

    # Constraint: Ensure a unit of any job can be assigned to a timeslot only if slot is active (open)
    def job_assignment_rule(model, t, j):
        return model.x[t, j] <= model.y[t]
    model.job_assignment_rule = pyo.Constraint(model.timeslots, model.jobs, rule=job_assignment_rule)

    # Constraint: Ensure at most G units of jobs can be assigned to an active (open) timeslot
    def parallel_job_assignment_rule(model, t):
        return sum(model.x[t, j] for j in model.jobs) <= model.y[t] * model.G
    model.parallel_job_assignment_rule = pyo.Constraint(model.timeslots, rule=parallel_job_assignment_rule)

    # Constraint: Ensure processing_times[j] units of a job j get assigned to active slots.
    def processing_time_assignment_rule(model, j):
        return sum(model.x[t, j] for t in model.timeslots) == model.processing_times[j]
    model.processing_time_assignment_rule = pyo.Constraint(model.jobs, rule=processing_time_assignment_rule)

    solver = SolverFactory("cplex_direct")
    results = solver.solve(model)
    # print(model.objective())
    # model.display()
    if results.solver.termination_condition == 'infeasible':
        schedule = Schedule(False,
                            perturbed_instance.number_of_parallel_jobs,
                            perturbed_instance.number_of_jobs,
                            perturbed_instance.number_of_timeslots)
        return schedule

    else:

        schedule = Schedule(True,
                            perturbed_instance.number_of_parallel_jobs,
                            perturbed_instance.number_of_jobs,
                            perturbed_instance.number_of_timeslots)

        for j in model.jobs:
            for t in model.timeslots:
                if model.x[t, j]() == 1:
                    # Schedule job j at timeslot t in the solution.
                    schedule.add_mapping(j, t)
        schedule.set_variables_changes(
            sum(sum((model.x[t, j]() - nominal_solution.schedule[j][t]) ** 2 for t in model.timeslots) for j in model.jobs)
        )
        return schedule
