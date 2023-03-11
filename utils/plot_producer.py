import os
import matplotlib.pyplot as plt
import seaborn as sns

from utils.parsing import construct_df_from_files


class PlotProducer:
    """
    Custom Class to assist with creating plots using seaborn and matplotlib.
    """

    def __init__(self, result_files: list, file_name: str, dataset_name: str, perturbation_enabled: bool = False):
        # Create data folders if they do not exist
        if not os.path.exists(f"data/plots/{dataset_name}"):
            os.makedirs(f"data/plots/{dataset_name}")

        # Merge files in a dataframe object
        if not perturbation_enabled:
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
        else:
            self.df = construct_df_from_files(result_files, "perturbation_results")
            self.df = self.df.rename(columns={"rmse_value": "RMSE"})
        self.file_name = file_name
        self.dataset_name = dataset_name

    def generate_line_plot(self, x: str, y: str, x_label: str, y_label: str, labels=None):
        plt.clf()
        sns.color_palette("Spectral", as_cmap=True)
        sns.lineplot(x=f"{x}", y=f"{y}", hue="Method", data=self.df)
        # sns.scatterplot(x=f"{x}", y=f"{y}", data=self.df, hue="Method", legend=False)
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

    def generate_scatter_plot(self, x: str, y: str, x_label: str, y_label: str):
        plt.clf()
        sns.scatterplot(data=self.df, x=f"{x}", y=f"{y}")
        plt.xlabel(f"{x_label}")
        plt.ylabel(f"{y_label}")
        plt.savefig(os.path.join(os.getcwd(),
                                 "data",
                                 "plots",
                                 f"{self.dataset_name}",
                                 f"{self.file_name}"))

    def generate_strip_plot(self, x: str, y: str, x_label: str, y_label: str):
        new_df = self.df[self.df["epsilon"] == 0.75]
        plt.clf()
        sns.stripplot(data=new_df, x=f"{x}", y=f"{y}", s=5, hue="Method", alpha=0.5, jitter=0.2)
        sns.despine()
        plt.xlabel(f"{x_label}")
        plt.ylabel(f"{y_label}")
        plt.savefig(os.path.join(os.getcwd(),
                                 "data",
                                 "plots",
                                 f"{self.dataset_name}",
                                 f"{self.file_name}"))

    def generate_swarm_plot(self, x: str, y: str, x_label: str, y_label: str):
        plt.clf()
        sns.swarmplot(data=self.df, x=f"{x}", y=f"{y}", s=2, hue="Method")
        sns.despine()
        plt.xlabel(f"{x_label}")
        plt.ylabel(f"{y_label}")
        plt.savefig(os.path.join(os.getcwd(),
                                 "data",
                                 "plots",
                                 f"{self.dataset_name}",
                                 f"{self.file_name}"))

    def generate_displot(self, x: str, x_label: str, col: str):
        plt.clf()
        sns.displot(data=self.df, x=f"{x}", hue="Method", kind="kde", fill=True).set(xlim=0)
        plt.xlabel(x_label)
        plt.savefig(os.path.join(os.getcwd(),
                                 "data",
                                 "plots",
                                 f"{self.dataset_name}",
                                 f"{self.file_name}"))

    def generate_scatter_plot2(self, x: str, y: str, x_label: str, y_label: str):
        new_df = self.df[self.df["gamma"] == 5]
        plt.clf()
        sns.scatterplot(data=new_df, x=f"{x}", y=f"{y}", hue="Method")
        plt.ylabel(f"{y_label}")
        plt.xlabel(f"{x_label}")
        plt.savefig(os.path.join(os.getcwd(),
                                 "data",
                                 "plots",
                                 f"{self.dataset_name}",
                                 f"{self.file_name}"))
