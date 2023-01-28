import argparse
import json
import logging
import os

from input_generation.dataset_generator import DatasetGenerator

# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Parse script arguments
parser = argparse.ArgumentParser(description="Program to generate data set with instances with changes in a specified "
                                             "parameter")

parser.add_argument("--name", help="Specify a name for the dataset.", default="default_dataset_name")
parser.add_argument("--T_range", help="list of timeslots separated with commas (e.g. 1,10,100)", default="100")
parser.add_argument("--G_range", help="list of batch-sizes separated with commas (e.g. 1,10,100)", default="5")
parser.add_argument("--J_range", help="list of jobs separated with commas (e.g. 1,10,100)", default="100")
parser.add_argument("--P", help="parameter of interest: G, T or J", default="100")
parser.add_argument("--N", help="number of instances to generate for each parameter", default=5)

args = parser.parse_args()


def generate_dataset_with_random_instances():
    """
    Generate a custom problem instance inside a json file that can be then used by solvers given
    a provided set of command-line arguments.

    Use: python3 -m input_generation.scripts.generate_random_instances --T_range "25, 50, 100, 150, 250, 500" --P "T" --name "test"

    """
    number_of_timeslots_lst = args.T_range.split(",")
    number_of_parallel_jobs_lst = args.G_range.split(",")
    number_of_jobs_lst = args.J_range.split(",")
    parameter_to_change = args.P

    logging.debug(number_of_timeslots_lst)
    logging.debug(number_of_parallel_jobs_lst)
    logging.debug(number_of_jobs_lst)
    logging.debug(parameter_to_change)
    logging.debug(f"Attempting to create a data set containing instances with changes in {args.P}")

    instances = []
    if parameter_to_change == "G":
        for param in number_of_parallel_jobs_lst:
            instances = instances + (
                DatasetGenerator.generate_multiple_feasible_instances(int(args.N),
                                                                      "Feasible_instances",
                                                                      int(number_of_jobs_lst[0]),
                                                                      int(number_of_timeslots_lst[0]),
                                                                      int(param)))

    elif parameter_to_change == "T":
        for param in number_of_timeslots_lst:
            instances = instances + (
                DatasetGenerator.generate_multiple_feasible_instances(int(args.N),
                                                                      "Feasible_instance",
                                                                      int(number_of_jobs_lst[0]),
                                                                      int(param),
                                                                      int(20 *
                                                                          int(number_of_parallel_jobs_lst[0]) / 100)
                                                                      ))

    elif parameter_to_change == "J":
        for param in number_of_jobs_lst:
            instances = instances + (
                DatasetGenerator.generate_multiple_feasible_instances(int(args.N),
                                                                      "Feasible_instance",
                                                                      int(param),
                                                                      int(number_of_timeslots_lst[0]),
                                                                      int(number_of_parallel_jobs_lst[0])
                                                                      ))

    # Check if directory is present
    if not os.path.exists('data/feasible_sets'):
        os.makedirs('data/feasible_sets')
    try:
        for instance in instances: print(instance.to_dict())
        path = f"data/feasible_sets/{args.name}.json"
        with open(path, "w") as f:
            json.dump({
                "dataset_name": f"{args.name}",
                "instances": [instance.to_dict() for instance in instances]
            }, f, indent=4)
        logging.info(f"Successfully created data set file: {path}")

    except:
        logging.error("Failed to create json file, try again.")
        return


generate_dataset_with_random_instances()
