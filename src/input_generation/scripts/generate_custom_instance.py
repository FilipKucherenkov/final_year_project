import argparse
import logging
import os

from problem_classes.problem_instances.custom_instance import CustomInstance
from utils.file_writers import write_instance_to_file

# Set log level
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

# Parse script arguments
parser = argparse.ArgumentParser(description="Script for generating custom problem instances and writing them to JSON "
                                             "files under data/custom_instances/ ")

parser.add_argument("--name", help="Specify a name for the problem instance file", default="default_instance_name")
parser.add_argument("--T", help="Specify the number of time slots", default="100")
parser.add_argument("--G", help="Specify the batch limit", default="100")
parser.add_argument("--jobs", help="Specify jobs in the form of comma separated string tuples (job_release: int, "
                                   "job_deadline: int, job_processing: int),... ")
args = parser.parse_args()


def generate_custom_problem_instance():
    """
    Generate a custom problem instance inside a json file that can be then used by solvers given
    a provided set of command-line arguments.
    """
    number_of_timeslots = int(args.T)
    number_of_parallel_jobs = int(args.G)

    logging.debug(f"T provided by user: {number_of_timeslots}")
    logging.debug(f"G provided by user: {number_of_parallel_jobs}")

    # Create a new problem instance with the provided properties
    new_problem_instance = CustomInstance(number_of_timeslots, number_of_parallel_jobs)

    for i, property_tuple in enumerate(args.jobs.split(",")):
        print(property_tuple)
        job_properties = property_tuple.split("-")
        release_time = int(job_properties[0])
        deadline = int(job_properties[1])
        processing_time = int(job_properties[2])

        new_problem_instance.add_job(i, release_time, deadline, processing_time)

    # Check if directory is present
    if not os.path.exists('data/custom_instances'):
        os.makedirs('data/custom_instances')

    write_instance_to_file(new_problem_instance, args.name, f"data/custom_instances/{args.name}.json")


generate_custom_problem_instance()
