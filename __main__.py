from input_generation.analysis_input_generator import AnalysisInputGenerator
from input_generation.custom_instance import CustomInstance
from input_generation.generate_input_data import generate_input_data
from solvers.models.active_time_ip import solve_active_time_ip
from solvers.models.maxflow_with_parameters import solve_max_flow
from solvers.solver_handler import solve_instance
from structures.graph.generate_network import generate_network


def main():
    instance1 = AnalysisInputGenerator.generate_feasible_instance("Large set", 1000)

    # instance22 = ProblemInstance("Small set")
    # solve_active_time_ip(instance22)
    # # instance3 = ProblemInstance("Moderate set", -1)
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
    instance3 = CustomInstance(6, 12, 1)

    instance3.add_job(0, 0, 2, 1)
    instance3.add_job(1, 0, 4, 1)
    instance3.add_job(2, 0, 6, 1)
    # instance3.add_job(3, 4, 10, 4)
    # instance3.add_job(4, 5, 9, 3)
    # instance3.add_job(5, 0, 4, 4)
    # instance3.add_job(6, 4, 8, 4)
    # instance3.add_job(7, 4, 8, 4)
    #
    # for job in instance3.jobs: print(job.processing_time)
    #
    # #

    # IP model computes 1
    schedule = solve_instance(instance3, "active-time-ip", "gurobi")
    schedule.print_schedule_info()
    # Greedy computes 3
    schedule2 = solve_instance(instance3, "greedy-maxflow", "gurobi")
    schedule2.print_schedule_info()
    # Maxflow model computes 3
    network = generate_network(instance3.time_horizon.time_slots, instance3.jobs)
    network.print_network_info()
    total_sum = sum(job.processing_time for job in instance3.jobs)
    schedule = solve_max_flow(network, total_sum, "gurobi")
    schedule.print_schedule_info()








main()
