import random

from algorithms.greedy_with_blackbox_heuristic import test, test_network
from models.active_time_ip import solve_active_time_ip
from models.max_flow import solve_max_flow
from models.max_flow_test import solve_max_flow_test
from structures.problem_instance import ProblemInstance
import matplotlib.pyplot as plt
import numpy as np


def main():
    # # instance1: ProblemInstance = ProblemInstance(12, 4, 3)
    # # execution_time = solve_active_time_ip(instance1)
    # execution_times = []
    # gs = []
    #
    # for i in range(2, 10):
    #     for j in range(2, 20):
    #         t = random.randint(20, 30)
    #         instance1: ProblemInstance = ProblemInstance(t, j, i)
    #         execution_time = solve_active_time_ip(instance1)
    #         gs.append(i)
    #         execution_times.append(execution_time)
    #
    # x = np.array(execution_times)
    # y = np.array(gs)
    # colors = np.array([i * 10 for i in range(1, len(gs) + 1)])
    #
    # plt.scatter(x, y, c=colors, cmap='viridis')
    # plt.show()
    test_network()
    # solve_max_flow()


main()
