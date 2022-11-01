import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from structures.problem_instance import ProblemInstance


def solve_active_time_ip(instance: ProblemInstance):
    """
    Pyomo model for Integer Programming definition given in Chang et al 2017.
    :return:
    """
    # Create pyomo model
    model = pyo.ConcreteModel()

    # Parameter: Number of jobs to be done in parallel TODO: Add those from method for generating data
    model.G = pyo.Param(initialize=instance.number_of_parallel_jobs)

    # Parameter: Number of timeslots TODO: Add those from method for generating data
    model.timeslots = instance.get_timeslots_lst()
    # Parameter: Jobs to be scheduled TODO: Add those from method for generating data
    model.jobs = instance.get_jobs_lst()

    # Parameter: Release times for jobs TODO: Add those from method for generating data
    model.release_times = pyo.Param(model.jobs, initialize=instance.get_job_release_times_map())
    release_times = model.release_times
    # Parameter: Deadlines for jobs TODO: Add those from method for generating data
    model.deadlines = pyo.Param(model.jobs, initialize=instance.get_job_deadlines_map())
    deadlines = model.deadlines
    # Parameter: Processing times for jobs TODO: Add those from method for generating data
    model.processing_times = pyo.Param(model.jobs, initialize=instance.get_processing_times_map())
    processing_times = model.processing_times

    # Decision variable: Whether slot t is open
    model.y = pyo.Var(model.timeslots, domain=pyo.Binary)
    y = model.y
    # Decision variable: Whether any unit of job j is assigned to slot t
    model.x = pyo.Var(model.timeslots, model.jobs, domain=pyo.Binary)
    x = model.x

    # Objective function: Minimise the number of active (open) timeslots
    def Objective_rule(model):
        return sum(y[t] for t in model.timeslots)

    model.objective = pyo.Objective(rule=Objective_rule, sense=pyo.minimize)

    # Constraint: Ensure a unit of any job can be assigned to a timeslot only if slot is active (open)
    @model.Constraint(model.timeslots, model.jobs)
    def job_assignment_rule(model, t, j):
        return x[t, j] <= y[t]

    # Constraint: Ensure at most G units of jobs can be assigned to an active (open) timeslot
    @model.Constraint(model.timeslots)
    def parallel_job_assignment_rule(model, t):
        return sum([model.x[t, j] for j in model.jobs]) <= model.G * y[t]

    # Constraint: Ensure processing_times[j] units of a job j get assigned to active slots.
    @model.Constraint(model.jobs)
    def processing_time_assignment_rule(model, j):
        return sum(x[t, j] for t in model.timeslots) >= processing_times[j]

    # Constraint: Ensure a job is not assigned to a timeslot if that timeslot is not within the job's window
    # (e.g. release_times[j],...,deadlines[j] )
    @model.Constraint(model.timeslots, model.jobs)
    def job_window_assignment_rule(model, t, j):
        if release_times[j] > t or deadlines[j] <= t:
            return x[t, j] == 0
        else:
            return pyo.Constraint.Skip

    solver = SolverFactory('gurobi')
    results = solver.solve(model)

    if results.solver.termination_condition == 'infeasible':
        print("No feasible solution found")
    else:
        print(f"Number of active time slots: {model.objective()}")
        print(f"Execution time: {results.solver.time}")
        for t in model.timeslots:
            for j in model.jobs:
                if(x[t,j]() != 0):
                    print("Job ", j, " scheduled in timeslot ", t, ": ", x[t, j]())
