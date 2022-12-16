from matplotlib.lines import Line2D
import numpy as np
import os

from input_generation.problem_instances.problem_instance import ProblemInstance
import matplotlib.pyplot as plt


# Generate Scatter plot to visualize where on the time horizon were
# the release times and deadlines generated
def generate_plot_for_input_generation(instance: ProblemInstance):
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.grid()
    plt.title("Generated release times and deadlines for jobs")
    plt.xlabel("Time Horizon")
    plt.xlim(0, instance.number_of_timeslots + 5)
    plt.ylim(0, 3)

    y = [0, 1, 2, 3]
    yticks = ["", "Release", "Deadline", ""]
    plt.yticks(y, yticks)
    plt.ylabel = ["Release", "Deadlines"]

    for job in instance.jobs:
        release_time_x = [job.release_time]
        release_time_y = [1]
        deadline_x = [job.deadline]
        deadline_y = [2]

        release_time_label = f"{job.number}"
        deadline_label = f"{job.number}"

        jitter_r_x = jitter_x_value(release_time_x)
        jitter_r_y = jitter_y_value(release_time_y)
        plt.plot(jitter_r_x, jitter_r_y, marker="o", markersize=7,
                 markeredgecolor="green",
                 markerfacecolor="green", label="deadline")
        plt.annotate(release_time_label, xy=(jitter_r_x, jitter_r_y), xytext=(jitter_r_x + 0.02,
                                                                              jitter_r_y + 0.02), fontsize=8)

        jitter_d_x = jitter_x_value(deadline_x)
        jitter_d_y = jitter_y_value(deadline_y)
        plt.plot(jitter_d_x, jitter_d_y, marker="o", markersize=7, markeredgecolor="red",
                 markerfacecolor="red", label="release")
        plt.annotate(deadline_label, xy=(jitter_d_x, jitter_d_y), xytext=(jitter_d_x + 0.02,
                                                                          jitter_d_y + 0.02), fontsize=8)

    red_circle = Line2D([0], [0], marker='o', color='w', label='Job deadlines',
                        markerfacecolor='r', markersize=15),
    green_circle = Line2D([0], [0], marker='o', color='w', label='Job release times',
                          markerfacecolor='g', markersize=15),

    colors = ["red", "green"]
    lines = [Line2D([0], [0], color=c, markersize=10, marker="o") for c in colors]
    labels = ["Job deadlines", "Job release times"]
    # red_patch = mpatches.Patch(color="red", label="Job deadlines", marker="o")
    # green_patch = mpatches.Patch(color="green", label='Job release times', marker="o")
    plt.legend(lines, labels, loc="upper left")
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "input_generation",
                             "plots",
                             f"instance_{instance.instance_type}"))


# Add some noise to a value x to avoid clustering
def jitter_x_value(x):
    if x == 0:
        x = x + 0.2
    return x + 0.1 * np.random.rand(len(x)) - 0.05


# Add some noise to a value y to avoid clustering
def jitter_y_value(y):
    random_op = np.random.randint(0, 100)
    if random_op > 40:
        return y + 0.4 * np.random.rand(len(y)) - 0.1
    else:
        return y - 0.3 * np.random.rand(len(y)) - 0.1
