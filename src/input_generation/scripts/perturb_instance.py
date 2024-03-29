import argparse
import logging
import os

from input_generation.perturbator import Perturbator


# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Parse script arguments
parser = argparse.ArgumentParser(description='Script to perturb a problem instance and write the perturbed instance'
                                             'to a JSON file.')

parser.add_argument("--gamma", help="Specify an upper bound on the perturbed jobs.", default="10")
parser.add_argument("--epsilon", help="Specify the degree of uncertainty.", default="1.0")
parser.add_argument("--instance_file", help="Specify the name of a file containing nominal instance to be perturbed.")
args = parser.parse_args()


def perturb_instance(instance_name: str, gamma: int, epsilon: float):
    if not os.path.exists(f"data/nominal_instances/{instance_name}.json"):
        logging.error(f"Nominal instance with that ID does not exist: {instance_name}")
        return

    p = Perturbator(f"data/nominal_instances/{instance_name}.json")
    p.perturb_instance(gamma, epsilon)


perturb_instance(args.instance_file, int(args.gamma), float(args.epsilon))
