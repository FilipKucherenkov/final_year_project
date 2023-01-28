import copy

from problem_classes.problem_instances import ParsedInstance
from problem_classes.scheduling.schedule import Schedule


def earliest_released_first(instance: ParsedInstance):
    """
    Simple greedy_algorithms algorithm which schedules each job at its release time, ignoring the
    capacity constraints.
    :param instance: parsed problem instance.
    :return: Schedule object containing the job to timeslot mappings.
    """
    job_to_timeslot_mapping = []

    # 0. Note: Important to deep copy input to avoid modifying problem instance.
    jobs = copy.deepcopy(instance.jobs)
    for job in jobs:
        # 1. Schedule each job at its release time, ignoring capacity constraint.
        for i in range(0, job.processing_time):

            job_to_timeslot_mapping.append((f"Job_{job.number}", f"Slot_{job.release_time + i}"))

    return Schedule(True, job_to_timeslot_mapping, instance.number_of_parallel_jobs)
