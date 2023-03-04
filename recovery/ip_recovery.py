import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from problem_classes.scheduling.recovery_schedule import RecoverySchedule
from problem_classes.scheduling.schedule import Schedule


def recover_schedule(perturbed_instance, nominal_solution, nominal_instance, solver_type):
    """
     Integer programming model for recovering from a solution of a nominal instance
     to a solution for a perturbed instance.
     :param perturbed_instance: ParsedInstance object for the perturbed instance.
     :param nominal_solution: Schedule object for the solution to the nominal instance.
     :param solver_type: specified solver to use (e.g. cplex-direct or gurobi)
     :return: Schedule object containing the recovered solution.
    """

    # Create Pyomo model
    model = pyo.ConcreteModel()
    model.name = "Recovery Method for R-ATSP"

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

    # Decision variable: Whether slot t is open
    model.y = pyo.Var(model.timeslots, bounds={0, 1}, within=pyo.Binary)
    # Decision variable: Whether any unit of job j is assigned to slot t
    model.x = pyo.Var(model.timeslots, model.jobs, bounds={0, 1}, within=pyo.Binary)
    model.G = pyo.Var(within=pyo.NonNegativeIntegers)

    # Pre-processing step
    for j in range(0, len(nominal_solution.schedule)):
        row = nominal_solution.schedule[j]
        total_p = 0
        for t in range(0, len(row)):
            if sum(row) > model.processing_times[j]:
                # Job reduction
                if nominal_solution.schedule[j][t] == 1:
                    if total_p >= model.processing_times[j]:
                        continue
                    else:
                        model.x[t, j].fix(1)
                        model.y[t].fix(1)
                        total_p = total_p + 1
            else:
                # Job augmentation
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
    model.multi_objective = pyo.Objective(rule=objective_rule, sense=pyo.minimize)

    # def c_1(model):
    #     return model.y[t] * model.G <= model.l2
    # model.c_1 = pyo.Constraint(rule=c_1)
    # #
    # def c_2(model):
    #     return sum(model.y[t] for t in model.timeslots) <= model.l3
    # model.c_2 = pyo.Constraint(rule=c_2)
    # #
    # def c_3(model):
    #     return sum(sum((nominal_solution.schedule[j][t] - model.x[t,j])**2 for t in model.timeslots) for j in model.jobs) <= model.l1
    # model.c_2 = pyo.Constraint(rule=c_3)

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

    solver = SolverFactory("gurobi")
    results = solver.solve(model)
    model.display()
    if results.solver.termination_condition == 'infeasible':
        schedule = RecoverySchedule(False,
                                    nominal_instance.number_of_parallel_jobs,
                                    perturbed_instance.number_of_jobs,
                                    perturbed_instance.number_of_timeslots)
        return schedule

    else:
        print(f"++++++{nominal_instance.number_of_parallel_jobs}")
        schedule = RecoverySchedule(True,
                                    nominal_instance.number_of_parallel_jobs,
                                    perturbed_instance.number_of_jobs,
                                    perturbed_instance.number_of_timeslots)

        job_to_timeslot_mapping = []
        for j in model.jobs:
            for t in model.timeslots:
                if model.x[t, j]() == 1:
                    # Schedule job j at timeslot t in the solution.
                    schedule.add_mapping(j, t)
                    print((f"Job_{j}", f"Slot_{t}"))
                    job_to_timeslot_mapping.append((f"Job_{j}", f"Slot_{t}"))

        # return Schedule(True, job_to_timeslot_mapping, instance.number_of_parallel_jobs)

        return schedule