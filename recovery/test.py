import math

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from problem_classes.scheduling.recovery_schedule import RecoverySchedule
from problem_classes.scheduling.schedule import Schedule


def recovery_method(perturbed_instance, solution, solver_type):
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


    model.l1 = pyo.Var(within=pyo.NonNegativeIntegers, initialize=0)
    model.l2 = pyo.Var(within=pyo.NonNegativeIntegers, initialize=2)
    model.l3 = pyo.Var(within=pyo.NonNegativeIntegers, initialize=1)

    # Ensure a job is not assigned to a timeslot if that timeslot is not within the job's window
    for t in model.timeslots:
        for j in model.jobs:
            if t < pyo.value(model.release_times[j]) or t >= pyo.value(model.deadlines[j]):
                model.x[t, j].fix(0)
    #
    # for j in range(0, len(solution.schedule)):
    #     row = solution.schedule[j]
    #     total_p = 0
    #     for t in range(0, len(row)):
    #             # Job reduction
    #             # print(sum(row))
    #             # print(model.processing_times[j])
    #         # print(f"Job {j}, Timeslot: {t}")
    #         # print(sum(row))
    #         # print(model.processing_times[j])
    #
    #         if sum(row) > model.processing_times[j]:
    #             # job reduction
    #             if solution.schedule[j][t] == 1:
    #                 if total_p >= model.processing_times[j]:
    #                     continue
    #                 else:
    #                     # Job reduction
    #                     model.x[t, j].fix(1)
    #                     model.y[t].fix(1)
    #                     total_p = total_p + 1
    #         else:
    #             # job augmentation
    #             if solution.schedule[j][t] == 1:
    #                 # Job augmentation
    #                 model.x[t, j].fix(1)
    #                 model.y[t].fix(1)

    # Objective function: Minimise the number of active (open) timeslots
    def objective_rule_1(model):
        # return sum(model.y[t] * model.G for t in model.timeslots)
        return sum(model.y[t] for t in model.timeslots)
    model.objective_rule_1 = pyo.Objective( rule=objective_rule_1, sense=pyo.minimize)

    # # Objective function: Minimise the number of active (open) timeslots
    def objective_rule_2(model):
        return sum(model.y[t] * model.G for t in model.timeslots)
        # return sum(model.y[t] for t in model.timeslots)
    model.objective_rule_2 = pyo.Objective(rule=objective_rule_2, sense=pyo.minimize)

    def objective_rule_3(model):
        print(solution.schedule)
        return sum(sum((solution.schedule[j][t] - model.x[t,j])**2 for t in model.timeslots) for j in model.jobs)
        # return sum(model.y[t] for t in model.timeslots)
    model.objective_rule_3 = pyo.Objective(rule=objective_rule_3, sense=pyo.minimize)

    # def multi_objective(model):
    #     return model.l1 + model.l2 + model.l3
    # model.multi_objective = pyo.Objective(rule=multi_objective, sense=pyo.minimize)
    #
    # def c_1(model):
    #     return model.y[t] * model.G <= model.l2
    # model.c_1 = pyo.Constraint(rule=c_1)
    #
    # def c_2(model):
    #     return sum(model.y[t] for t in model.timeslots) <= model.l3
    # model.c_2 = pyo.Constraint(rule=c_2)
    #
    # def c_3(model):
    #     return sum(sum((solution.schedule[j][t] - model.x[t,j])**2 for t in model.timeslots) for j in model.jobs) <= model.l1
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


    # def job_augmentation_rule(model, j):
    #     return sum(solution.schedule[j][t] + model.x[t,j] for t in model.timeslots) <= model.processing_times[j]
    #
    # model.processing_time_assignment_rule = pyo.Constraint(model.jobs, rule=job_augmentation_rule)
    # Constraint: Ensure a job is not assigned to a timeslot if that timeslot is not within the job's window
    # (e.g. release_times[j],...,deadlines[j] )
    # def job_window_assignment_rule(model, t, j):
    #     if t in (model.release_times[j], model.deadlines[j]):
    #         return pyo.Constraint.Skip
    #     else:
    #         return model.x[t, j] == 0
    # model.job_window_assignment_rule = pyo.Constraint( model.timeslots, model.jobs, rule=job_window_assignment_rule)

    solver = SolverFactory("gurobi")
    # solver.options['mipgap'] = 0000000.1  # Set gap tolerance to 0.01
    # solver.options['NonConvex'] = 2

    model.objective_rule_3.deactivate()
    model.objective_rule_2.deactivate()
    results = solver.solve(model)
    print(results)

    model.objective_rule_2.activate()
    model.objective_rule_3.deactivate()
    model.objective_rule_1.deactivate()
    results2 = solver.solve(model)
    print(results2)

    model.objective_rule_2.deactivate()
    model.objective_rule_3.activate()
    model.objective_rule_1.deactivate()
    results3 = solver.solve(model)
    print(results3)


    if results.solver.termination_condition == 'infeasible':
        schedule = Schedule(False, [], perturbed_instance.number_of_parallel_jobs)
        return schedule

    else:

        schedule = RecoverySchedule(True,
                                    solution.batch_limit,
                                    perturbed_instance.number_of_jobs,
                                    perturbed_instance.number_of_timeslots)

        job_to_timeslot_mapping = []
        for j in model.jobs:
            for t in model.timeslots:
                if model.x[t, j]() == 1:
                    # Schedule job j at timeslot t in the solution.
                    schedule.add_mapping(j, t)
                    job_to_timeslot_mapping.append((f"Job_{j}", f"Slot_{t}"))

        # return Schedule(True, job_to_timeslot_mapping, instance.number_of_parallel_jobs)

        return schedule
