import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from problem_classes.scheduling.schedule import Schedule


def solve_active_time_ip(instance: ParsedInstance, solver_type: str):
    """
    Create and solve Pyomo model for Integer programming formulation given by Chang et al. 2017
    :param instance: Problem instance object
    :param solver_type: specified solver to use (e.g. cplex-direct or gurobi)
    :return:
    """

    # Create Pyomo model
    model = pyo.ConcreteModel()
    model.name = "IP model for Active Time Scheduling problem"

    # Parameter: Set of timeslots.
    model.timeslots = pyo.Set(initialize=instance.get_timeslots_lst())
    # Parameter: Set of jobs
    model.jobs = pyo.Set(initialize=instance.get_jobs_lst())

    # Parameter: Number of jobs to be done in parallel.
    model.G = pyo.Param(within=pyo.NonNegativeIntegers, initialize=instance.number_of_parallel_jobs)
    # Parameter: Release times for jobs.
    model.release_times = pyo.Param(model.jobs, within=pyo.NonNegativeReals,
                                    initialize=instance.get_job_release_times_map())

    # Parameter: Deadlines for jobs.
    model.deadlines = pyo.Param(model.jobs, within=pyo.NonNegativeReals,
                                initialize=instance.get_job_deadlines_map())
    # Parameter: Processing times for jobs.
    model.processing_times = pyo.Param(model.jobs, within=pyo.NonNegativeReals,
                                       initialize=instance.get_processing_times_map())

    # Decision variable: Whether slot t is open
    model.y = pyo.Var(model.timeslots, bounds={0, 1}, within=pyo.Binary)
    # Decision variable: Whether any unit of job j is assigned to slot t
    model.x = pyo.Var(model.timeslots, model.jobs, bounds={0, 1}, within=pyo.Binary)

    # Ensure a job is not assigned to a timeslot if that timeslot is not within the job's window
    for t in model.timeslots:
        for j in model.jobs:
            if t < pyo.value(model.release_times[j]) or t >= pyo.value(model.deadlines[j]):
                model.x[t, j].fix(0)

    # Objective function: Minimise the number of active (open) timeslots
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

    # Constraint: Ensure a job is not assigned to a timeslot if that timeslot is not within the job's window
    # (e.g. release_times[j],...,deadlines[j] )
    # def job_window_assignment_rule(model, t, j):
    #     if t in (model.release_times[j], model.deadlines[j]):
    #         return pyo.Constraint.Skip
    #     else:
    #         return model.x[t, j] == 0
    # model.job_window_assignment_rule = pyo.Constraint( model.timeslots, model.jobs, rule=job_window_assignment_rule)

    solver = SolverFactory(solver_type)
    results = solver.solve(model)
    # print(results)
    model.display()

    if results.solver.termination_condition == 'infeasible':
        schedule = Schedule(False, [], instance.number_of_parallel_jobs)
        return schedule

    else:
        job_to_timeslot_mapping = []
        for t in model.timeslots:
            for j in model.jobs:

                if model.x[t, j]() == 1:
                    # Schedule job j at timeslot t in the solution.
                    job_to_timeslot_mapping.append((f"Job_{j}", f"Slot_{t}"))

        return Schedule(True, job_to_timeslot_mapping, instance.number_of_parallel_jobs)
