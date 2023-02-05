import argparse
import json
import logging
import os

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from solvers.solver_handler import solve_instance
from stats.analysis_helpers.helpers import record_execution_time_on_instance

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def record_solver_performance():
    """
    Record the performance of a solver on a given data set.
    User can choose: algorithm, dataset, solver and type of analysis.

    python3 -m stats.scripts.record_solver_performance --file "data/feasible_sets/instances_with_changes_in_batch_size_set.json" --analysis_type "runtime" --algorithm "Greedy-local-search: CPLEX Re-optimization"

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
        results["instance_results"] = []
        logging.info(f"Recording {args.algorithm} runtime on {dataset_name}...")
        for i, instance in enumerate(instances):
            time_taken = record_execution_time_on_instance(instance, args.algorithm, args.solver_type)
            results["instance_results"] = results["instance_results"] + [{
                "Algorithm": f"{args.algorithm}",
                "Instance_index": f"instance_{i}",
                "ID": instance.instance_id,
                "T": instance.number_of_timeslots,
                "G": instance.number_of_parallel_jobs,
                "J": instance.number_of_jobs,
                "runtime_in_sec": time_taken}]

    # Record objective value performance.
    elif args.analysis_type == "objective":
        results["instance_results"] = []
        logging.info(f"Recording {args.algorithm} objective value on {dataset_name}...")
        for i, instance in enumerate(instances):
            schedule = solve_instance(instance, args.algorithm, args.solver_type)
            results["instance_results"] = results["instance_results"] + [{
                "Algorithm": f"{args.algorithm}",
                "Instance_index": f"instance_{i}",
                "ID": instance.instance_id,
                "T": instance.number_of_timeslots,
                "G": instance.number_of_parallel_jobs,
                "J": instance.number_of_jobs,
                "objective_value": schedule.calculate_active_time(),
                "batch_utilization": schedule.calculate_batch_utilization_ratio()}]

    logging.info(f"Results recorded successfully")

    # Generate folder if it does not exist.
    if not os.path.exists(f"data/results/{args.analysis_type}"):
        os.makedirs(f"data/results/{args.analysis_type}")
    if not os.path.exists(f"data/results/{args.analysis_type}/{args.algorithm}"):
        os.makedirs(f"data/results/{args.analysis_type}/{args.algorithm}")
    try:
        path = f"data/results/{args.analysis_type}/{args.algorithm}/results_{dataset_name}.json"
        with open(path, "w") as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results recorded successfully: {path}")

    except:
        logging.error("Failed to create json file with results")
        return


record_solver_performance()
