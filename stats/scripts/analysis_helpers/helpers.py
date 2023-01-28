import logging
import timeit
import json
import pandas as pd

from problem_classes.problem_instances import ParsedInstance
from solvers.solver_handler import solve_instance


def record_execution_time_on_instance(instance: ParsedInstance, algorithm: str, solver_type: str):
    t = timeit.Timer(lambda: solve_instance(instance, algorithm, solver_type))
    times = t.repeat(3, 3)
    total_time_taken = min(times) / 3
    return total_time_taken


def construct_df_from_files(files: list[str], json_field: str):
    """
    Given a list of paths to json files, construct a DataFrame object with the
    data from the parsed files for further analysis.
    :param json_field: field from json to normalize the data
    :param files: list of strings (file paths to json files).
    :return: DataFrame object containing the parsed data.
    """
    # Parse json
    dataframes = []

    for file in files:
        try:
            with open(file) as json_file:
                data = json.load(json_file)

                dataframes.append(pd.DataFrame.from_dict(pd.json_normalize(data[json_field])))
                logging.info(f"Successfully loaded json file: {file}")
        except:
            logging.error(f"Failed to parse json, please try again: {file}")
            return

    df = pd.concat(dataframes)
    return df
