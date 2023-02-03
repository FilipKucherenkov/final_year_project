import copy

from problem_classes.problem_instances.parsed_instance import ParsedInstance
from problem_classes.scheduling.schedule import Schedule


def erf_with_density_heuristic(instance: ParsedInstance):
    """
    Simple algorithm based on Earliest-Released-First-Strategy that uses 2 heuristics

    Heuristic 2: Before scheduling a job at its release time, check whether there is a more dense interval
    within its window (a point where more jobs are scheduled). If yes, schedule the job unit at the current most dense
    point. If no such point is available schedule it at its current release time. O(n^2)
    :param instance: parsed problem instance.
    :return: Schedule object containing the job to timeslot mappings.
    """
    job_to_timeslot_mapping = []
    density_map = {}  # stores interval densities

    # Note: Important to deep copy input to avoid modifying problem instance.
    jobs = copy.deepcopy(instance.jobs)

    # Sort jobs based on Heuristic 1.
    jobs.sort(key=lambda j: (j.deadline - j.release_time) / j.processing_time)

    for job in jobs:
        used_intervals = []

        new_interval = _get_most_dense_interval_within_window(job, density_map, used_intervals)
        total_processing = job.processing_time
        while total_processing > 0 and new_interval != -1:
            job_to_timeslot_mapping.append((f"Job_{job.number}", f"Slot_{new_interval}"))

            # Mark interval as used
            used_intervals.append(new_interval)
            # Find a new dense interval
            new_interval = _get_most_dense_interval_within_window(job, density_map, used_intervals)
            total_processing = total_processing - 1

        if total_processing == 0:
            continue

        else:
            # Schedule a job at its release time
            for i in range(0, total_processing):
                current_release = job.release_time

                # If time slot has been used by job skip it
                while current_release in used_intervals:
                    current_release = current_release + 1

                # Update density map
                if current_release + i in density_map:
                    density_map[current_release + i] = density_map[current_release + i] + 1
                else:
                    density_map[current_release + i] = 1

                job_to_timeslot_mapping.append((f"Job_{job.number}", f"Slot_{current_release + i}"))

    return Schedule(True, job_to_timeslot_mapping, instance.number_of_parallel_jobs)


def _get_most_dense_interval_within_window(job, density_map, used_intervals):
    """
    Find the most dense unused interval within a job's window.
    """

    curr_release_time = job.release_time
    max_count = -1
    best_t = -1
    while curr_release_time < job.deadline:

        if curr_release_time in used_intervals:
            curr_release_time = curr_release_time + 1
            continue

        if curr_release_time in density_map and density_map[curr_release_time] >= max_count:
            max_count = density_map[curr_release_time]
            best_t = curr_release_time
        curr_release_time = curr_release_time + 1

    return best_t
