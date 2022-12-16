from input_generation.generate_input_data import parse_data_set
from input_generation.problem_instances.custom_instance import CustomInstance
from stats.algorithms.execution_times.compare_execution_times_from_dataset \
    import compare_running_times_on_dataset_with_varying_number_of_jobs
from structures.graph.generate_network import test


def main():
    # solve_active_time_ip(instance22)
    # instance1.print_instance_info()
    # network = generate_network(instance1.time_horizon.time_slots, instance1.jobs)
    # network.print_network_info()
    # instance = CustomInstance(6, 12, 100000)
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
    instance3 = CustomInstance(3, 12, 3)

    instance3.add_job(0, 0, 2, 2)
    instance3.add_job(1, 0, 2, 2)
    instance3.add_job(2, 0, 4, 2)
    instance3.add_job(3, 0, 6, 4)
    instance3.add_job(4, 0, 6, 4)
    instance3.add_job(5, 0, 12, 2)
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

    # # Maxflow model computes 3

    # schedule, flow_values = solve_max_flow(instance3, "gurobi")
    # schedule.print_schedule_info()
    # for k, v in flow_values.items():
    #     print(k, v)

    # generate_plot_for_input_generation(instance22)
    # generate_input_data()

    # Generate running time plot
    # generate_line_plot_for_running_times()
    #
    # s = solve_instance(instance3, "Greedy-local-search-with-warm-start", "gurobi")
    # s.print_schedule_info()
    # solve_instance(instance3, "Active-time-IP", "gurobi")
    instances, dataset_name = parse_data_set("data/feasible_sets/instances_with_changing_number_of_jobs_set.json")
    # compare_running_times_on_dataset_with_changes_in_batch_size(instances, dataset_name)
    # generate_input_data()
    compare_running_times_on_dataset_with_varying_number_of_jobs(instances, "maxflow_comparison")

    # network = generate_network(instance3.time_horizon.time_slots, instance3.jobs)
    # j_sum = sum(job.processing_time for job in instance3.jobs)
    # schedule = solve_maxflow_cplex(network.arcs, network.source_node, network.sink_node, j_sum)
    # schedule2 = solve_max_flow(instance3, "gurobi")
    # schedule.print_schedule_info()
    # schedule2.print_schedule_info()
    # schedule3 = solve_instance(instance3, "Active-time-IP", "gurobi")
    # schedule3.print_schedule_info()
    # schedule4 = solve_instance(instance3, "Greedy-local-search-with-opt", "cplex")
    # schedule4.print_schedule_info()

    # schedule3 = solve_instance(instance3, "Greedy-local-search-with-opt-v2", "cplex")
    # schedule3.print_schedule_info()
    # schedule4 = solve_instance(instance3, "Greedy-local-search-with-reopt", "cplex")
    # schedule4.print_schedule_info()
    # test()


main()
