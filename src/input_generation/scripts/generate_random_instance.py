import argparse
import logging
import os

from problem_classes.problem_instances.problem_instance import ProblemInstance
from utils.file_writers import write_instance_to_file

# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Parse script arguments
parser = argparse.ArgumentParser(
    description='Script to generate a random problem instance and write it to a json file.')

parser.add_argument("--name", help="Specify a name for the file", default="default_instance_name")
parser.add_argument("--T", help="specify the number of time slots", default="100")
parser.add_argument("--G", help="specify the batch limit", default="100")
parser.add_argument("--J", help="specify the number of jobs", default="100")
args = parser.parse_args()


def generate_random_problem_instance():
    """
    Generate a random problem instance inside a json file that can be then used by solvers given
    a provided set of command-line arguments.
    example command:
    python3 -m input_generation.scripts.generate_random_instance --name "user_guide_example_2" --T 100 --G 5 --J 20
    """
    number_of_timeslots = int(args.T)
    number_of_parallel_jobs = int(args.G)
    number_of_jobs = int(args.J)

    logging.debug(f"T provided by user: {number_of_timeslots}")
    logging.debug(f"G provided by user: {number_of_parallel_jobs}")
    logging.debug(f"J provided by user: {number_of_jobs}")

    # Create a new random problem instance with the provided properties
    new_problem_instance = ProblemInstance(f"{args.name}", number_of_jobs, number_of_timeslots, number_of_parallel_jobs)

    # Check if directory is present
    if not os.path.exists('data/random_instances'):
        os.makedirs('data/random_instances')

    write_instance_to_file(new_problem_instance, args.name, f"data/random_instances/{args.name}.json")


generate_random_problem_instance()
