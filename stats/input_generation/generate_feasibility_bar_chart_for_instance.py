import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from input_generation.problem_instances.parsed_instance import ParsedInstance


def generate_feasibility_bar_chart_for_dataset(dataset: list[ParsedInstance]):
    """
    Generate a barchart showing how many instances are feasible and how many are not in a dataset
    :param dataset: list of parsed problem instances.
    """
    stats = generate_instance_stats(dataset)

    agr = stats.groupby(["Instance type", "Schedule"]).size().reset_index(name="Occurrences")

    ax = sns.barplot(x="Instance type", y="Occurrences", hue="Schedule", errorbar=None, data=agr)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))  # Force integer ticks
    plt.title("Generated instances")
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(os.getcwd(),
                             "stats",
                             "input_generation",
                             "plots",
                             "feasibility_bar"))


def generate_instance_stats(instances):
    """
    Given a parsed problem instance, return a df object containing its type and whether is feasible.
    """
    stats = []
    for i in instances:
        is_feasible = i.is_feasible()
        stats.append({
            "Instance type": i.instance_type,
            "Schedule": "Feasible" if is_feasible else "Infeasible"
        })

    df = pd.DataFrame(stats)
    return df
