from algorithms.greedy_with_blackbox_heuristic import test_network, greedy_with_blackbox_heuristic
from input_generation.analysis_input_generator import AnalysisInputGenerator

from input_generation.problem_instance import ProblemInstance
from models.active_time_ip import solve_active_time_ip
from stats.algorithms.execution_times.time_average_execution_time import generate_line_plot_for_running_times
from stats.input_generation.generate_feasibility_bar_chart_for_instance import \
    generate_feasibility_bar_chart_for_instance


def main():
    # instance1 = AnalysisInputGenerator.generate_infeasible_instance("Small set", -1)

    # # instance2 = ProblemInstance("Moderate set", -1)
    # # instance3 = ProblemInstance("Moderate set", -1)
    # instance1.print_instance_info()
    # network = generate_network(instance1.time_horizon.time_slots, instance1.jobs)
    # network.print_network_info()
    # instance = CustomInstance(6, 12, 2)
    # instance.add_job(0, 0, 2, 2)
    # instance.add_job(1, 0, 4, 2)
    # instance.add_job(2, 1, 6, 1)
    # instance.add_job(3, 4, 10, 4)
    # instance.add_job(4, 5, 9, 3)
    # instance.add_job(5, 0, 4, 4)
    #
    # instance2 = CustomInstance(6, 12, 2)
    # instance2.add_job(0, 0, 2, 2)
    # instance2.add_job(1, 0, 4, 2)
    # instance2.add_job(2, 0, 4, 4)

    # test_network()
    # schedule = solve_active_time_ip(instance1)
    # schedule.print_schedule_info()
    # generate_plot_for_input_generation(instance1)
    # print(instance1.is_feasible())
    # schedule = greedy_with_blackbox_heuristic(instance1)
    # schedule2 = solve_active_time_ip(instance1)
    # schedule2.print_schedule_info()
    # schedule.print_schedule_info()
    # plot_average_execution_time()
    # generate_feasibility_bar_chart_for_instance()
    generate_line_plot_for_running_times()

main()
