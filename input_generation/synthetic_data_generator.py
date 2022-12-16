import math
import random

from structures.scheduling.job import Job


class SyntheticDataGenerator:
    """
    SyntheticDataGenerator class containing static methods for generating input data following the Synthetic Data
    Generator Approach.
    """

    @staticmethod
    def generate_jobs(n: int) -> list[Job]:
        """
        Generate jobs
        :param n: Number of jobs to be generated.
        :return: a list of jobs in the form [0, 1, ... , n]
        """
        jobs: list[Job] = []

        for i in range(0, n):
            jobs.append(Job(i))
        return jobs

    @staticmethod
    def generate_release_times_for_jobs(jobs: list[Job], t: int, alpha: float = 0.9) -> None:
        """
        Given a list of jobs, generate a randon release time for each job
        :param jobs: jobs to receive release times
        :param t: number of discrete timeslots.
        :param alpha: alpha parameter for random generation. (Default value is 0.9).
        Note: Alpha closer to 0 is clustering release times towards the beginning of the horizon
        """

        for job in jobs:
            random_time = random.randint(0, math.ceil(alpha * t))
            job.release_time = random_time

    @staticmethod
    def generate_deadlines_for_jobs(jobs: list[Job], t: int, alpha: float = 0.0001) -> None:
        """
        Given a list of jobs, generate a random deadline for each job
        :param jobs: jobs to receive deadlines
        :param t: number of discrete timeslots.
        :param alpha: alpha parameter for random generation. (Default value is 0.1).
        """

        for job in jobs:
            random_time = random.randint(math.floor(job.release_time * (1 + alpha)), t)
            job.deadline = random_time

    @staticmethod
    def generate_processing_times_for_jobs(jobs: list[Job]) -> None:
        """
        Given a list of jobs, generate a random processing time for each jobs
        Note: beta value at random from the interval (0,1) and set each job processing time p(j) = ceiling(beta*(d(j)-r(j)).
        :param jobs: jobs to receive deadlines
        """
        beta: float = random.uniform(0.01, 1)

        for job in jobs:
            random_time = math.ceil(beta * (job.deadline - job.release_time))
            job.processing_time = random_time
