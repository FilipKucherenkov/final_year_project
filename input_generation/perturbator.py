import math
import random

from utils.file_writers import write_instance_to_file
from utils.parsing import parse_problem_instance


class Perturbator:

    def __init__(self, json_file: str):
        problem_instance = parse_problem_instance(json_file)
        self.problem_instance = problem_instance

    # epsilon - specifies the degree of uncertainty
    # gamma - specifies ub on jobs to be perturbed
    def perturb_instance(self, gamma: float, eps: float):
        number_of_perturbations = math.floor(random.uniform(0, gamma))

        print(f"Gamma: {gamma}, #Perturbs: {number_of_perturbations}")
        for i in range(0, number_of_perturbations):
            # Choose a random job to perturb it from the instance
            random_index = random.randint(0, len(self.problem_instance.jobs) - 1)
            target_job = self.problem_instance.jobs[random_index]

            p = target_job.processing_time
            d = target_job.deadline
            r = target_job.release_time
            epsilon = random.uniform((p-1) / p, (d-r-1-2*p)/p)
            print(f"epsilon {epsilon}")
            target_job.processing_time = math.floor(random.uniform((1 - epsilon) * p, (1 + epsilon) * p))
            print(f"Perturbing job: {target_job.number}")
            print(f"Perturbation: from {p} to {target_job.processing_time}")

        print(self.problem_instance.instance_id)
        # # Write the perturbed instance to a file
        write_instance_to_file(self.problem_instance, "perturbation")
