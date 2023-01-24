from input_generation.generate_input_data import parse_data_set, generate_data_set_with_varying_t_length
from input_generation.problem_instances.custom_instance import CustomInstance
from solvers.models.maxflow_cplex_with_reopt import solve_maxflow_cplex_with_reopt
from solvers.solver_handler import solve_instance
from stats.algorithms.execution_times.compare_execution_times_from_dataset \
    import compare_running_times_on_dataset_with_varying_number_of_jobs, \
    compare_running_times_on_dataset_with_changes_in_t
from stats.scripts.analyse_solver_results import  compare_running_times_for_greedy_local_search, \
    compare_runtime_on_dataset_1, compare_runtime_on_dataset_2, compare_utilization_perc_on_dataset_2
from structures.graph.generate_network import test


def main():
    # solve_active_time_ip(instance22)
    # instance1.print_instance_info()
    # network = generate_network(instance1.time_horizon.time_slots, instance1.jobs)
    # network.print_network_info()
    # instance = CustomInstance( 12, 3)
    # instance.add_job(0, 0, 2, 2)
    # instance.add_job(1, 0, 4, 2)
    # instance.add_job(2, 1, 6, 1)
    # instance.add_job(3, 4, 10, 4)
    # instance.add_job(4, 5, 9, 3)
    # instance.add_job(5, 0, 4, 4)
    #
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
    # IP model computes 1
    # schedule = solve_instance(instance3, "active-time-ip", "gurobi")
    # schedule.print_schedule_info()
    #
    #
    # # Greedy computes 3
    # test_network()

    # schedule = solve_maxflow_cplex_with_reopt(instance)
    # schedule2 = schedule = solve_instance(instance, "Active-time-IP", "gurobi")
    # schedule.print_schedule_info()
    # schedule2.print_schedule_info()

    compare_runtime_on_dataset_1("Runtime_on_dataset_1")
    compare_runtime_on_dataset_2("Runtime_on_dataset_2")
    compare_utilization_perc_on_dataset_2("Batch_util_on_dataset_2")
    compare_running_times_for_greedy_local_search("Greedy_comparison")

main()
