import argparse
import json
import logging
import os

from input_generation.problem_instances.parsed_instance import ParsedInstance
from solvers.solver_handler import solve_instance
from stats.scripts.analysis_helpers.helpers import record_execution_time_on_instance

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def record_solver_performance():
    """
    Record the performance of a solver on a given data set.
    User can choose: algorithm, dataset, solver and type of analysis.
    """
    # Parse script arguments
    parser = argparse.ArgumentParser(description='Script that records performance')

    parser.add_argument("--algorithm", help="Specify solver", default="Active-time-IP")
    parser.add_argument("--file", help="Provide the path to a json file containing a dataset")
    parser.add_argument("--solver_type", help="Choose optimization solver to be utilized", default="cplex_direct")
    parser.add_argument("--analysis_type", help="Choose analysis type: runtime, objective", default="runtime")

    args = parser.parse_args()

    logging.info('Validating provided arguments...')
    # Validate that correct file was provided
    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        logging.error(f"Please specify correct path to data set file: {args.file}")
        return

    # Attempt to parse dataset
    instances, dataset_name = parse_data_set(args.file)
    results = {"algorithm": args.algorithm, "data_set_name": dataset_name}
    logging.info("Data set parsed successfully")

    # Record runtime performance
    if args.analysis_type == "runtime":
        results["runtime"] = {}
        logging.info(f"Recording {args.algorithm} runtime on {dataset_name}...")
        for i, instance in enumerate(instances):
            time_taken = record_execution_time_on_instance(instance, args.algorithm, args.solver_type)
            results["runtime"][f"instance_{i}"] = time_taken

    # Record objective value performance.
    elif args.analysis_type == "objective":
        results["objective_value"] = {}
        logging.info(f"Recording {args.algorithm} objective value on {dataset_name}...")
        for i, instance in enumerate(instances):
            schedule = solve_instance(instance, args.algorithm, args.solver_type)
            results["objective_value"][f"instance_{i}"] = schedule.calculate_active_time()

    logging.info(f"Results recorded successfully")

    # Generate folder if it does not exist.
    if not os.path.exists(f"data/results/{args.analysis_type}"):
        os.makedirs(f"data/results/{args.analysis_type}")
    if not os.path.exists(f"data/results/{args.analysis_type}/{args.algorithm}"):
        os.makedirs(f"data/results/{args.analysis_type}/{args.algorithm}")
    try:
        path = f"data/results/{args.analysis_type}/{args.algorithm}/{args.algorithm}-on-{dataset_name}.json"
        with open(path, "w") as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results recorded successfully: {path}")

    except:
        logging.error("Failed to create json file with results")
        return


def parse_data_set(file_name):
    """
    Given a file path containing a dataset, parse it to a list of ParsedInstance objects for further processing.
    :param file_name: str for the file path to the dataset file.
    :return: list of ParsedInstance objects.
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


record_solver_performance()
