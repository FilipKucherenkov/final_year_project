from problem_classes.problem_instances.custom_instance import CustomInstance
from solvers.solver_handler import solve_instance
from stats.scripts.analyse_solver_results import generate_all_plots


def main():
    # solve_active_time_ip(instance22)
    # instance1.print_instance_info()
    # network = generate_network(instance1.time_horizon.time_slots, instance1.jobs)
    # network.print_network_info()
    instance = CustomInstance(12, 3)
    instance.add_job(0, 0, 2, 2)
    instance.add_job(1, 0, 4, 2)
    instance.add_job(2, 1, 6, 1)
    instance.add_job(3, 4, 10, 4)
    instance.add_job(4, 5, 9, 3)
    instance.add_job(5, 0, 4, 4)

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
    # # # # schedule2 = solve_instance(instance, "Active-time-IP", "gurobi")
    # schedule.print_schedule_info()
    # schedule2.print_schedule_info()

    generate_all_plots()


main()
