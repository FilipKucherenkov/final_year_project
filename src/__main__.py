from input_generation.perturbator import Perturbator
from problem_classes.graph.generate_network import generate_network
from problem_classes.problem_instances.custom_instance import CustomInstance
from solvers.recovery.ip_recovery_3 import ip_recovery3
from solvers.recovery_handler import recover_schedule

from solvers.solver_handler import solve_instance
from utils.plot_functions import print_objective_performance_for_recovery, print_objective_performance_on_all_datasets
from utils.statistics import print_all_recovery_stats, print_rmse_stats_for_methods


def main():
    # Small custom example
    instance = CustomInstance(12, 3)
    instance.add_job(0, 0, 2, 2)
    instance.add_job(1, 0, 4, 3)
    instance.add_job(2, 1, 6, 1)
    instance.add_job(3, 4, 10, 4)
    instance.add_job(4, 5, 9, 3)
    instance.add_job(5, 0, 4, 4)

    # Generate the custom instance's corresponding flow network and print properties
    # network = generate_network(instance.time_horizon.time_slots, instance.jobs)
    # network.print_network_info()

    # Solve custom instance using deterministic IP Model and print schedule.
    # schedule1 = solve_instance(instance, "Active-time-IP", "cplex_direct")
    # schedule1.print_schedule_info()

    # Solve custom instance using GLS with Pyomo model.
    # schedule2 = solve_instance(instance, "Greedy-local-search: Pyomo", "cplex_direct")
    # schedule2.print_schedule_info()

    # Solve custom instance using GLS with CPLEX model (V1).
    # schedule3 = solve_instance(instance, "Greedy-local-search: CPLEX (V1)", "cplex_direct")
    # schedule3.print_schedule_info()

    # Solve custom instance using GLS with CPLEX model (V2).
    # schedule4 = solve_instance(instance, "Greedy-local-search: CPLEX (V2)", "cplex_direct")
    # schedule4.print_schedule_info()

    # Solve custom instance using GLS with Re-Opt.
    # schedule5 = solve_instance(instance, "Greedy-local-search: CPLEX Re-optimization", "cplex_direct")
    # schedule5.print_schedule_info()

    # Solve custom instance using ERF.
    # schedule6 = solve_instance(instance, "Earliest-released-first", "cplex_direct")
    # schedule6.print_schedule_info()

    # Solve custom instance using Density Heuristic.
    # schedule7 = solve_instance(instance, "Earliest-released-first-with-density-heuristic", "cplex_direct")
    # schedule7.print_schedule_info()

    # Same instance from Figure 4.1 in Chapter 4.
    nominal_instance = CustomInstance(7, 2)
    nominal_instance.add_job(0, 4, 6, 2)
    nominal_instance.add_job(1, 0, 4, 4)
    nominal_instance.add_job(2, 0, 4, 1)
    nominal_instance.add_job(3, 0, 2, 2)

    # Job 2 changes its processing time from 1 to 4 in the true scenario.
    perturbed_instance = CustomInstance(7, 2)
    perturbed_instance.add_job(0, 4, 6, 2)
    perturbed_instance.add_job(1, 0, 4, 4)
    perturbed_instance.add_job(2, 0, 4, 4)
    perturbed_instance.add_job(3, 0, 2, 2)

    # Recover schedule (Note this example is tight and the choice of weights does not make difference)
    # On the other hand, it illustrates the effectiveness of the Capacity Search Method.
    recovered_solution = recover_schedule(nominal_instance, perturbed_instance, 1, 1, 1)
    recovered_solution.print_schedule_info()

    # rmse_gamma_displot_moderate_instance("Active-time-IP", "Greedy-local-search: CPLEX Re-optimization")
    # rmse_gamma_scatter("Active-time-IP", "Greedy-local-search: CPLEX Re-optimization")

    # compute_stats_and_produce_plots()
    # compute_stats_and_produce_plots()
    # print_nominal_instances_stats()
    # compute_stats_and_produce_plots()
    #
    # print_all_recovery_stats()


def compute_stats_and_produce_plots():
    # Calculate Root Mean Square Error (RMSE) value for results.
    # opt_rmse: Compares solution produced on nominal instance compared to opt on perturbed. (Nominal Solution Quality)
    # rmse: Compares solution produced on nominal compared to solution on perturbed. (Sensitivity)
    # print_rmse_stats_for_methods()

    # Prints performance of a specific method on dataset.
    # Available methods:
    # 1. Earliest-released-first
    # 2. Earliest-released-first-with-density-heuristic
    # 3. Maxflow-LP
    # 4. Greedy-local-search: CPLEX Re-optimization
    # print_objective_performance_on_all_datasets("Active-time-IP")

    # Prints performance of IP Model and GLS Method combined with recovery method.
    print_objective_performance_for_recovery()


main()
