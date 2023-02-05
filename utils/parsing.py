import json
import logging
import pandas as pd

from problem_classes.problem_instances.parsed_instance import ParsedInstance


def parse_data_set(file_name):
    """
    Given a file path containing a dataset, parse it to a list of ParsedInstance objects for further processing.
    :param file_name: str for the file path to the dataset file.
    :return: list of ParsedInstance objects and the name of the dataset.
    """
    # Open dataset file.
    f = open(file_name)

    # Parse data.
    data = json.load(f)
    f.close()

    instance_list: list[ParsedInstance] = []
    for instance_info in data["instances"]:
        # Create a ParsedInstance object for each problem instance in the dataset.
        instance_list.append(ParsedInstance(instance_info))

    return instance_list, data["dataset_name"]


def parse_problem_instance(file_name):
    """
    Given a path to a json file containing a problem instance, parse it.
    :param file_name: str for the file path to the instance file.
    :return: Parsed instance object
    """
    # Open instance file.
    f = open(file_name)

    # Parse data.
    data = json.load(f)
    f.close()

    # Create a ParsedInstance object for each problem instance in the dataset.
    new_instance = ParsedInstance(data["instance"])
    logging.info("Successfully parsed instance file: {}".format(data["instance_name"]))
    return new_instance


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
