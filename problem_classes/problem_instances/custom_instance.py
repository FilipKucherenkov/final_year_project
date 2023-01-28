import uuid
from solvers.models.maxflow_pyomo import solve_max_flow_model
from problem_classes.graph.generate_network import generate_network
from problem_classes.scheduling.job import Job
from problem_classes.scheduling.time_horizon import TimeHorizon


class CustomInstance:
    """
    Simple class to represent a problem instance of the Active time scheduling problem. This class is used to generate
    manual test cases to better study algorithm/model performance.

    Note: Getter methods are used to assist with feeding input to optimization models.
    """

    def __init__(self, number_of_timeslots, number_of_parallel_jobs: int):
        self.number_of_timeslots = number_of_timeslots
        self.number_of_jobs = 0
        self.number_of_parallel_jobs = number_of_parallel_jobs
        # Generate time horizon
        self.time_horizon = TimeHorizon(self.number_of_timeslots, number_of_parallel_jobs)
        # Jobs are empty initially
        self.jobs = []

        # Generate a unique instance id
        self.instance_id = str(uuid.uuid4())

    # Checks feasibility of instance based on a Max-flow computation
    def is_feasible(self):
        network = generate_network(self.time_horizon.time_slots, self.jobs)
        total_sum = sum(job.processing_time for job in self.jobs)
        schedule = solve_max_flow_model(network, total_sum, self)
        return schedule.is_feasible

    # Create a new Job and add it to the problem instance
    def add_job(self, job_number: int, job_release: int, job_deadline: int, job_processing: int):
        new_job = Job(job_number)
        new_job.release_time = job_release
        new_job.deadline = job_deadline
        new_job.processing_time = job_processing
        self.number_of_jobs += 1
        self.jobs.append(new_job)

    # Return a list containing the start times of each timeslot (e.g 0,1,2...)
    def get_timeslots_lst(self) -> list[int]:
        timeslots_list: list[int] = []
        for i in range(0, self.number_of_timeslots + 1):
            timeslots_list.append(i)
        return timeslots_list

    # Return a list containing the job numbers (e.g. job names)
    def get_jobs_lst(self) -> list[int]:
        job_names: list[int] = []
        for job in self.jobs:
            job_names.append(job.number)
        return job_names

    # Return a dictionary containing a key value pair of
    # the form Key: Job number, Value: Job release time
    def get_job_release_times_map(self) -> dict[int]:
        release_times: dict[int] = {}
        for job in self.jobs:
            release_times[job.number] = job.release_time
        return release_times

    # Return a dictionary containing a key value pair of
    # the form Key: Job number, Value: Job deadline
    def get_job_deadlines_map(self) -> dict[int]:
        deadlines: dict[int] = {}
        for job in self.jobs:
            deadlines[job.number] = job.deadline
        return deadlines

    # Return a dictionary containing a key value pair of
    # the form Key: Job number, Value: Job processing time
    def get_processing_times_map(self) -> dict[int]:
        processing_times: dict[int] = {}
        for job in self.jobs:
            processing_times[job.number] = job.processing_time
        return processing_times

    # Convert a problem instance to dictionary
    def to_dict(self):
        problem_data = {
            "instance_id": self.instance_id,
            "number_of_jobs": self.number_of_jobs,
            "G": self.number_of_parallel_jobs,
            "T": self.number_of_timeslots,
            "jobs": [job.__dict__ for job in self.jobs],
        }
        return problem_data

    # Print information about jobs in this problem instance
    # (e.g. job number, release time, deadline, processing time...)
    def print_instance_info(self):
        for job in self.jobs:
            print(job.get_properties())
        print(self.time_horizon)
