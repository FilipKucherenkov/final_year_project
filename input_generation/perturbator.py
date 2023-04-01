import copy
import logging
import math
import random
import uuid

from utils.file_writers import write_perturbed_instance_to_file
from utils.parsing import parse_problem_instance


class Perturbator:
    """
    Class used for perturbing problem instances.
    """

    def __init__(self, json_file: str):
        problem_instance = parse_problem_instance(json_file)
        self.problem_instance = problem_instance

    # epsilon - specifies the degree of uncertainty
    # gamma - specifies ub on jobs to be perturbed
    def perturb_instance(self, gamma: int, epsilon: float):

        # Generate id for perturbation
        perturbation_id = str(uuid.uuid4())

        # Generate new instance
        new_instance = copy.deepcopy(self.problem_instance)

        # number_of_perturbations = math.floor(random.uniform(0, gamma))
        # Stats for the Perturbation
        number_of_perturbations = gamma
        number_of_augmentations = 0
        number_of_decreases = 0
        logging.info(f"User selected Gamma={gamma} and epsilon={epsilon}")
        # Perturb gamma jobs
        for i in range(0, gamma):
            # Choose a random job to perturb it from the instance
            random_index = random.randint(0, len(new_instance.jobs) - 1)
            target_job = new_instance.jobs[random_index]

            p = target_job.processing_time
            d = target_job.deadline
            r = target_job.release_time
            # epsilon = random.uniform((p-1) / p, (d-r-1-2*p)/p)
            new_p = math.floor(random.uniform((1 - epsilon) * p, (1 + epsilon) * p))

            # Ensure processing stays within bounds
            if new_p < 1:
                new_p = 1
            if new_p > d - r:
                new_p = d - r

            if new_p > p:
                # Job augmentation
                logging.info(f"Perturbing job: {target_job.number}, duration changed from {p} to {new_p} [Augmentation]")
                number_of_augmentations = number_of_augmentations + 1
            elif new_p < p:
                # Job decrease
                logging.info(f"Perturbing job: {target_job.number}, duration changed from {p} to {new_p} [Reduction]")
                number_of_decreases = number_of_decreases + 1
            else:
                # Nothing happens
                logging.info(f"Perturbing job: {target_job.number}, duration changed from {p} to {new_p} [No effect]")
                number_of_perturbations = number_of_perturbations - 1
            target_job.processing_time = new_p

        # All required stats
        perturbation_stats = {
            "gamma": gamma,
            "epsilon": epsilon,
            "perturbation_id": perturbation_id,
            "number_of_perturbed_jobs": number_of_perturbations,
            "number_of_job_augmentations": number_of_augmentations,
            "number_of_jobs_decreases": number_of_decreases,
            "batch_augmentation_is_required": not new_instance.is_feasible(),
        }
        # Write the perturbed instance to a JSON file
        write_perturbed_instance_to_file(new_instance,
                                         new_instance.instance_id,
                                         perturbation_stats,)

        return new_instance
