import copy

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from problem_classes.scheduling.schedule import Schedule


def erf_with_density_heuristic(instance: ParsedInstance):
    """
    Simple algorithm based on Earliest-Released-First-Strategy that uses 2 heuristics
    Heuristic 1: Sort jobs based on h(j) = (j.deadline - j.release_time) / j.processing_time
    Heuristic 2: Before scheduling a job at its release time, check whether there is a more dense release time
    within its window (a point where more jobs are scheduled). If yes, schedule the job at the most dense point. If no such
    point is available schedule it at its current release time. O(n^2)
    :param instance: parsed problem instance.
    :return: Schedule object containing the job to timeslot mappings.
    """
    job_to_timeslot_mapping = []

    # 0. Note: Important to deep copy input to avoid modifying problem instance.
    jobs = copy.deepcopy(instance.jobs)
    jobs.sort(key=lambda j: (j.deadline - j.release_time) / j.processing_time)
    for job in jobs:
        new_release_time = _get_most_dense_release_time(job, jobs)
        if new_release_time != -1:
            # 1. Schedule each job at its release time, ignoring capacity constraint.
            for i in range(0, job.processing_time):
                job_to_timeslot_mapping.append((f"Job_{job.number}", f"Slot_{new_release_time + i}"))
        else:
            for i in range(0, job.processing_time):
                job_to_timeslot_mapping.append((f"Job_{job.number}", f"Slot_{job.release_time + i}"))

    return Schedule(True, job_to_timeslot_mapping, instance.number_of_parallel_jobs)


def _get_most_dense_release_time(job, jobs):

    number_of_overlaps = {}
    for j in jobs:
        current_release = j.release_time

        if job.release_time < j.release_time and current_release + job.processing_time < job.deadline:
            if j.release_time not in number_of_overlaps:
                number_of_overlaps[j.release_time] = 1
            else:
                number_of_overlaps[j.release_time] = number_of_overlaps[j.release_time] + 1
    current_max = 0
    best_release = -1
    for new_release, overlap_count in number_of_overlaps.items():
        if overlap_count >= current_max:
            best_release = new_release
            current_max = overlap_count

    return best_release
