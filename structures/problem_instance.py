from structures.job import Job
from structures.synthetic_data_generator import SyntheticDataGenerator
from structures.time_horizon import TimeHorizon


class ProblemInstance:
    time_horizon: TimeHorizon
    jobs: list[Job]
    number_of_timeslots: int
    number_of_jobs: int
    number_of_parallel_jobs: int

    def __init__(self, number_of_timeslots: int, number_of_jobs: int, number_of_parallel_jobs: int):
        self.number_of_timeslots = number_of_timeslots
        self.number_of_jobs = number_of_jobs
        self.number_of_parallel_jobs = number_of_parallel_jobs

        # Generate time horizon
        self.time_horizon = TimeHorizon(number_of_timeslots)
        # Generate jobs
        self.jobs = SyntheticDataGenerator.generate_jobs(number_of_jobs)

        # Generate random properties for each job
        SyntheticDataGenerator.generate_release_times_for_jobs(self.jobs, number_of_timeslots)
        SyntheticDataGenerator.generate_deadlines_for_jobs(self.jobs, number_of_timeslots)
        SyntheticDataGenerator.generate_processing_times_for_jobs(self.jobs)

        for job in self.jobs:
            print(job.get_properties())
        print(self.time_horizon)

    def get_timeslots_lst(self) -> list[int]:
        timeslots_list: list[int] = []
        for i in range(0, self.number_of_timeslots + 1):
            timeslots_list.append(i)
        return timeslots_list

    def get_jobs_lst(self) -> list[int]:
        job_names: list[int] = []
        for job in self.jobs:
            job_names.append(job.number)
        return job_names

    def get_job_release_times_map(self) -> dict[int]:
        release_times: dict[int] = {}
        for job in self.jobs:
            release_times[job.number] = job.release_time
        return release_times

    def get_job_deadlines_map(self) -> dict[int]:
        deadlines: dict[int] = {}
        for job in self.jobs:
            deadlines[job.number] = job.deadline
        return deadlines

    def get_processing_times_map(self) -> dict[int]:
        processing_times: dict[int] = {}
        for job in self.jobs:
            processing_times[job.number] = job.processing_time
        return processing_times
