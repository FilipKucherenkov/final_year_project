import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from problem_classes.scheduling.recovery_schedule import Schedule


def recover_schedule(perturbed_instance, nominal_solution, capacity_limit, augmented_capacity):
    """
     IP Model with Binded Decisions
     :param perturbed_instance: ParsedInstance object representing the True Scenario
     (Scenario after uncertainty realisation)
     :param nominal_solution: Schedule object representing the solution to the Nominal Scenario
     (Scenario before uncertainty realisation)
     :param capacity_limit: int representing the initial batch capacity.
     :param augmented_capacity: int representing the augmented batch capacity.
     :return: Schedule object containing the recovered solution.
    """

    # Create Pyomo model
    model = pyo.ConcreteModel()
    model.name = "IP Model with Binded Decisions"

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
    model.G = pyo.Param(within=pyo.NonNegativeIntegers, initialize=augmented_capacity)

    # Decision variable: Whether slot t is open
    model.y = pyo.Var(model.timeslots, bounds={0, 1}, within=pyo.Binary)
    # Decision variable: Whether any unit of job j is assigned to slot t
    model.x = pyo.Var(model.timeslots, model.jobs, bounds={0, 1}, within=pyo.Binary)

    # Pre-processing step
    for j in range(0, len(nominal_solution.schedule)):
        row = nominal_solution.schedule[j]
        total_p = 0
        for t in range(0, len(row)):
            if sum(row) > model.processing_times[j]:
                # Processing Time Reduction
                if nominal_solution.schedule[j][t] == 1:
                    if total_p >= model.processing_times[j]:
                        continue
                    else:
                        model.x[t, j].fix(1)
                        model.y[t].fix(1)
                        total_p = total_p + 1
            else:
                # Processing Time Augmentation
                if nominal_solution.schedule[j][t] == 1:
                    model.x[t, j].fix(1)
                    model.y[t].fix(1)

    # Ensure a job is not assigned to a timeslot if that timeslot is not within the job's window
    for t in model.timeslots:
        for j in model.jobs:
            if t < pyo.value(model.release_times[j]) or t >= pyo.value(model.deadlines[j]):
                model.x[t, j].fix(0)

    def objective_rule(model):
        return sum(model.y[t] for t in model.timeslots)

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
    # model.display()
    if results.solver.termination_condition == 'infeasible':
        schedule = Schedule(False,
                            capacity_limit,
                            perturbed_instance.number_of_jobs,
                            perturbed_instance.number_of_timeslots)
        return schedule

    else:
        schedule = Schedule(True,
                            capacity_limit,
                            perturbed_instance.number_of_jobs,
                            perturbed_instance.number_of_timeslots)

        for j in model.jobs:
            for t in model.timeslots:
                if model.x[t, j]() == 1:
                    # Schedule job j at timeslot t in the solution.
                    schedule.add_mapping(j, t)

        return schedule
