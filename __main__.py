from problem_classes.problem_instances.custom_instance import CustomInstance

from solvers.recovery.two_stage_recovery import  two_stage_recovery
from solvers.solver_handler import solve_instance
from utils.statistics import print_rmse_stats_for_methods


def main():
    # solve_active_time_ip(instance22)
    # instance1.print_instance_info()
    # network = generate_network(instance1.time_horizon.time_slots, instance1.jobs)
    # network.print_network_info()
    instance = CustomInstance(12, 1)
    instance.add_job(0, 0, 2, 2)
    instance.add_job(1, 0, 4, 3)
    instance.add_job(2, 0, 2, 2)
    # instance.add_job(2, 1, 6, 1)
    # instance.add_job(3, 4, 10, 4)
    # instance.add_job(4, 5, 9, 3)
    # instance.add_job(5, 0, 4, 4)

    instance_with_overlaps = CustomInstance(12, 10)
    instance_with_overlaps.add_job(0, 0, 2, 2)
    instance_with_overlaps.add_job(1, 1, 3, 2)
    instance_with_overlaps.add_job(2, 4, 10, 2)

    p_i_1 = CustomInstance(7, 2)
    p_i_1.add_job(0, 4, 6, 2)
    p_i_1.add_job(1, 0, 4, 4)
    p_i_1.add_job(2, 0, 4, 2)
    p_i_1.add_job(3, 0, 2, 2)

    p_p_1 = CustomInstance(7, 2)
    p_p_1.add_job(0, 4, 6, 2)
    p_p_1.add_job(1, 0, 4, 4)
    p_p_1.add_job(2, 0, 4, 4)
    p_p_1.add_job(3, 0, 2, 2)

    # p_i_1 = CustomInstance(7, 1)
    # p_i_1.add_job(0, 0, 4, 1)
    # p_i_1.add_job(1, 0, 4, 1)
    # p_i_1.add_job(2, 0, 4, 1)
    # p_i_1.add_job(3, 0, 2, 1)
    #
    # p_p_1 = CustomInstance(7, 1)
    # p_p_1.add_job(0, 0, 4, 1)
    # p_p_1.add_job(1, 0, 4, 1)
    # p_p_1.add_job(2, 0, 6, 3)
    # p_p_1.add_job(3, 0, 2, 1)

    # instance = CustomInstance(12, 2)
    # instance.add_job(0, 0, 3, 2)
    # instance.add_job(0, 0, 3, 3)

    # instance2 = CustomInstance(6, 12, 10)
    # instance2.add_job(0, 0, 2, 2)
    # instance2.add_job(1, 0, 4, 2)
    # instance2.add_job(2, 0, 4, 4)
    # instance3 = CustomInstance(12, 3)
    #
    # instance3.add_job(0, 0, 2, 2)
    # instance3.add_job(1, 0, 2, 2)
    # instance3.add_job(2, 0, 4, 2)
    # instance3.add_job(3, 0, 6, 4)
    # instance3.add_job(4, 0, 6, 4)
    # instance3.add_job(5, 0, 12, 2)
    #
    # for job in instance3.jobs: print(job.processing_time)
    #
    # #
    # schedule = solve_instance(instance3, "Earliest-released-first", "gurobi")
    # schedule.print_schedule_info()
    #
    #
    # # Greedy computes 3
    # test_network()

    # schedule = solve_maxflow_cplex_with_reopt(instance)
    # schedule = solve_instance(instance, "Earliest-released-first-with-density-heuristic", "gurobi")
    # schedule2 = solve_instance(instance_2, "Active-time-IP", "gurobi")

    # schedule.print_schedule_info()
    # schedule2.print_schedule_info()
    # schedule = solve_instance(instance, "1", "gurobi")
    # schedule.print_schedule_info()
    # generate_all_plots()

    # # Perturb
    # p = Perturbator("data/custom_instances/small_instance_1.json")
    # p_initial = p.problem_instance
    # # opt_shedule = solve_instance(p_initial, "Greedy-local-search: CPLEX Re-optimization", "gurobi")
    # # # opt_shedule.print_schedule_info()
    # p_instance = p.perturb_instance(20, 50)
    # s_i = solve_instance(p_i_1, "Active-time-IP", "gurobi")
    # s_i.print_schedule_info()
    # s_p = solve_instance(p_instance, "Active-time-IP", "gurobi")
    # s_p.print_schedule_info()
    # s_i1 = solve_instance(p_i_1, "Active-time-IP", "gurobi")
    # s_i1.print_schedule_info()
    # s_r = recover_schedule(p_p_1, s_i, "gurobi")
    # s_r.print_schedule_info()

    # schedule2.print_schedule_info()
    # adversary_jobs = recover_with_back_filling(solve_instance(p_initial, "Active-time-IP", "gurobi"), p_instance)
    # for j in adversary_jobs:
    #     print(f"Job: {j.number}, p: {j.processing_time}")

    # schedule3.print_schedule_info()

    # s = solve_instance(p_initial, "Active-time-IP", "cplex_direct")
    # s.print_schedule_info()
    # s1 = solve_instance(p_instance, "Active-time-IP", "cplex_direct")
    # s1.print_schedule_info()
    # p = recovery_method(p_instance, s, "cplex_direct")
    # p.print_schedule_info()

    # s = solve_instance(instance_with_overlaps, "1", "gurobi")
    # s.print_schedule_info()
    # schedule4 = solve_instance(p_initial, "Active-time-IP", "gurobi")
    # # # # schedule3.print_schedule_info()
    # schedule4.print_schedule_info()

    # rmse_gamma_displot_large_instance("Active-time-IP", "Greedy-local-search: CPLEX Re-optimization")
    # rmse_gamma_displot_moderate_instance("Active-time-IP", "Greedy-local-search: CPLEX Re-optimization")
    # s = capacity_search(p_instance, 20)
    # s.print_schedule_info()
    # compute_stats_and_produce_plots()
    # compute_stats_and_produce_plots()

    s1 = solve_instance(p_i_1, "Active-time-IP", "gurobi")
    s2 = two_stage_recovery(p_p_1, s1, 1)
    s2.print_schedule_info()
    # rmse_gamma_displot_moderate_instance("Active-time-IP", "Greedy-local-search: CPLEX Re-optimization")
    # rmse_gamma_scatter("Active-time-IP", "Greedy-local-search: CPLEX Re-optimization")
    # s = recover_from_perturbation("IP with fixed variables", p_p_1, p_i_1, 1, "cplex_direct")
    # s = recover_schedule(p_p_1, None, None, "cplex_direct")
    # s1 = solve_instance(p_p_1, "Earliest-released-first-with-density-heuristic", "gurobi")
    # # s1 = solve_unbounded_ip(p_initial, "gurobi")
    # # s.print_schedule_info()
    # s1.print_schedule_info()
    #
    # compute_stats_and_produce_plots()
    # print_nominal_instances_stats()




def compute_stats_and_produce_plots():

    # Calculate Root Mean Square Error (RMSE) value for results
    # opt_rmse: Compares solution produced on nominal instance compared to opt on perturbed. (Recoverable-Robustness)
    # rmse: Compares solution produced on nominal compared to solution on perturbed. (Sensitivity)
    print_rmse_stats_for_methods()
    #
    # Available methods:
    # 1. Earliest-released-first
    # 2. Earliest-released-first-with-density-heuristic
    # 3. Maxflow-LP
    # 4. Greedy-local-search: CPLEX Re-optimization
    # print_objective_performance_on_all_datasets("Active-time-IP")


main()
