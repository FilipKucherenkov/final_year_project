import argparse
import logging
import os

from input_generation.perturbator import Perturbator


# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Parse script arguments
parser = argparse.ArgumentParser(description='A script to generate a random problem instance in a json file')

parser.add_argument("--gamma", help="Specify an upper bound on the perturbed jobs.", default="10")
parser.add_argument("--epsilon", help="Specify the degree of uncertainty.", default="1.0")
parser.add_argument("--instance_id", help="Specify the ID of a nominal instance to be perturbed.")
args = parser.parse_args()


# Check if file is present
#
def perturb_instance(instance_id, gamma, epsilon):
    if not os.path.exists(f"data/nominal_instances/{instance_id}.json"):
        logging.error(f"Nominal instance with that ID does not exist: {instance_id}")
        return

    p = Perturbator(f"data/nominal_instances/{instance_id}.json")
    p.perturb_instance(gamma, epsilon)


perturb_instance(args.instance_id, int(args.gamma), float(args.epsilon))
