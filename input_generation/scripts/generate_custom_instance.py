import argparse
import json
import os

from input_generation.problem_instances.custom_instance import CustomInstance

# Parse script arguments
parser = argparse.ArgumentParser(description='A program to generate problem instance in a json file')

parser.add_argument("--name", help="Give a name for your instance file", default="default_instance_name")
parser.add_argument("--T", help="number of time slots", default="100")
parser.add_argument("--G", help="number of time slots", default="100")
parser.add_argument("--jobs", help="jobs in the form of comma separated string tuples (job_release: int, "
                                   "job_deadline: int, job_processing: int),... ")
args = parser.parse_args()


def generate_custom_problem_instance():
    """
    Generate a custom problem instance inside a json file that can be then used by solvers given
    a provided set of command-line arguments.
    """
    number_of_timeslots = int(args.T)
    number_of_parallel_jobs = int(args.G)

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

    with open(f"data/custom_instances/{args.name}.json", "w") as f:
        json.dump({
            "instance_name": f"{args.name}",
            "instance": new_problem_instance.to_dict()
        }, f, indent=4)


generate_custom_problem_instance()