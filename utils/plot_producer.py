import os
import matplotlib.pyplot as plt
import seaborn as sns

from utils.parsing import construct_df_from_files


class PlotProducer:

    def __init__(self, result_files: list, file_name: str, dataset_name: str):
        # Create data folders if they do not exist
        if not os.path.exists(f"data/plots/{dataset_name}"):
            os.makedirs(f"data/plots/{dataset_name}")

        # Merge files in a dataframe object
        self.df = construct_df_from_files(result_files, "instance_results")
        self.df.rename(columns={"Algorithm": "Method"}, inplace=True)
        self.df["Method"] = self.df["Method"].map({
            "Active-time-IP": "Integer Programming Model",
            "Greedy-local-search: CPLEX Re-optimization": "Greedy Local Search (CPLEX Re-Opt)",
            "Greedy-local-search: CPLEX (V1)": "Greedy Local Search (CPLEX V1)",
            "Greedy-local-search: CPLEX (V2)": "Greedy Local Search (CPLEX V2)",
            "Greedy-local-search: Pyomo": "Greedy Local Search (Pyomo)",
            "Earliest-released-first": "Earliest Released First",
            "Maxflow-LP": "Max-Flow LP Model",
            "Earliest-released-first-with-density-heuristic": "Density Heuristic"
        })
        self.file_name = file_name
        self.dataset_name = dataset_name

    def generate_line_plot(self, x: str, y: str, x_label: str, y_label: str, labels=None):
        plt.clf()
        sns.color_palette("Spectral", as_cmap=True)
        sns.lineplot(x=f"{x}", y=f"{y}", hue="Method", data=self.df)
        sns.scatterplot(x=f"{x}", y=f"{y}", data=self.df, hue="Method", legend=False)
        # if labels:
        #     plt.legend(title="Method", labels=labels)
        # else:
        #     plt.legend(title="Method")

        # plt.legend(loc='upper right')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(os.path.join(os.getcwd(),
                                 "data",
                                 "plots",
                                 f"{self.dataset_name}",
                                 f"{self.file_name}"))

    def generate_bar_plot(self, x: str, y: str, x_label: str, y_label: str):
        plt.clf()
        sns.barplot(x=f"{x}", y=f"{y}", hue="Method", data=self.df, palette="magma")
        plt.xlabel(f"{x_label}")
        plt.ylabel(f"{y_label}")
        plt.savefig(os.path.join(os.getcwd(),
                                 "data",
                                 "plots",
                                 f"{self.dataset_name}",
                                 f"{self.file_name}"))

    def generate_scatter_plot(self):
        pass
