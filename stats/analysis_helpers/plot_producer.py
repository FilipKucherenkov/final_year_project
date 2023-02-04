import os

from stats.analysis_helpers.helpers import construct_df_from_files

import matplotlib.pyplot as plt
import seaborn as sns


class PlotProducer:

    def __init__(self, result_files: list, file_name: str):
        # Merge files in a dataframe object
        self.df = construct_df_from_files(result_files, "instance_results")
        self.file_name = file_name

    def generate_line_plot(self, x: str, y: str, x_label: str, y_label: str):
        plt.clf()
        sns.lineplot(x=f"{x}", y=f"{y}", hue="Algorithm", data=self.df)
        sns.scatterplot(x=f"{x}", y=f"{y}", data=self.df, hue="Algorithm", legend=False)
        # plt.legend(loc='upper right')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(os.path.join(os.getcwd(),
                                 "stats",
                                 "plots",
                                 f"{self.file_name}"))

    def generate_bar_plot(self,  x: str, y: str, x_label: str, y_label: str):
        plt.clf()
        sns.barplot(x=f"{x}", y=f"{y}", hue="Algorithm", data=self.df, palette="magma")
        plt.xlabel(f"{x_label}")
        plt.ylabel(f"{y_label}")
        plt.savefig(os.path.join(os.getcwd(),
                                 "stats",
                                 "plots",
                                 f"{self.file_name}"))

    def generate_scatter_plot(self):
        pass
