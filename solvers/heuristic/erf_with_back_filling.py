import copy

from input_generation.problem_instances.parsed_instance import ParsedInstance
from structures.scheduling.schedule import Schedule


def erf_with_back_filling(instance: ParsedInstance):
    """
    Simple algorithm which schedules each job at its release time, by marking the intervals as busy
    it then tries to back-fill with processing units from next jobs. This algorithm respects the capacity G. However,
    since it "back-fills" jobs to unused timeslots, it produces a worse solution in terms of the objective value.
    :param instance: parsed problem instance.
    :return: Schedule object containing the job to timeslot mappings.
    """
    job_to_timeslot_mapping = []

    # 0. Note: Important to deep copy input to avoid modifying problem instance.
    jobs = copy.deepcopy(instance.jobs)
    time_horizon_length = instance.time_horizon.t

    # Stores whether a timeslot is busy
    is_active = [[False for _ in range(time_horizon_length)] for _ in range(time_horizon_length)]

    # 2. Process jobs
    for job in jobs:
        processing_units = job.processing_time
        for row in range(0, len(is_active)):
            j = 0

            while processing_units > 0 and job.release_time + j < job.deadline:
                # slot is busy
                if not is_active[row][job.release_time + j]:
                    is_active[row][job.release_time + j] = True
                    job_to_timeslot_mapping.append((f"Job_{job.number}", f"Slot_{job.release_time + j}"))

                    processing_units = processing_units - 1
                j = j + 1

    return Schedule(True, job_to_timeslot_mapping, instance.number_of_parallel_jobs)
