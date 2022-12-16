import json

from input_generation.dataset_generator import DatasetGenerator
from input_generation.problem_instances.parsed_instance import ParsedInstance
import os


def generate_input_data():
    if not os.path.exists('data/feasible_sets'):
        os.makedirs('data/feasible_sets')

    feasible_instance_with_10_jobs = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 10, 100, 2)
    feasible_instance_with_25_jobs = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 25, 100, 5)
    feasible_instance_with_50_jobs = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 50, 100, 10)
    feasible_instance_with_100_jobs = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 20)
    feasible_instance_with_250_jobs = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 250, 100, 50)
    # feasible_instance_with_500_jobs = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 500, 100, 100)
    # feasible_instance_with_1000_jobs = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 1000, 100, 200)
    # feasible_instance_with_2000_jobs = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 2000, 100, 400)
    instances = feasible_instance_with_10_jobs + feasible_instance_with_25_jobs + feasible_instance_with_50_jobs + \
                feasible_instance_with_100_jobs + feasible_instance_with_250_jobs

    with open("data/feasible_sets/instances_with_changing_number_of_jobs_set.json", "w") as f:
        json.dump({
            "dataset_name": "instances_with_changing_number_of_jobs_set",
            "instances": [instance.to_dict() for instance in instances]
        }, f, indent=4)

    # instance_with_batch_size_2 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 2)
    # instance_with_batch_size_5 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 5)
    # instance_with_batch_size_10 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 10)
    # instance_with_batch_size_25 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 25)
    # instance_with_batch_size_50 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 50)
    # instance_with_batch_size_100 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 100)
    # instances = instance_with_batch_size_2 + instance_with_batch_size_5 + instance_with_batch_size_10 +\
    #             instance_with_batch_size_25 + instance_with_batch_size_50 + instance_with_batch_size_100
    #
    # with open("data/feasible_sets/instances_with_changes_in_batch_size_set.json", "w") as f:
    #     json.dump({
    #         "dataset_name": "instances_with_changes_in_batch_size_set",
    #         "instances": [instance.to_dict() for instance in instances]
    #     }, f, indent=4)

    # instance_with_batch_size_2 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 2)
    # instance_with_batch_size_5 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 5)
    # instance_with_batch_size_10 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 10)
    # instance_with_batch_size_25 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 25)
    # instance_with_batch_size_50 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 50)
    # instance_with_batch_size_100 = DatasetGenerator.generate_multiple_feasible_instances(1, "Small", 100, 100, 100)
    # instances = instance_with_batch_size_2 + instance_with_batch_size_5 + instance_with_batch_size_10 +\
    #             instance_with_batch_size_25 + instance_with_batch_size_50 + instance_with_batch_size_100
    #
    # with open("data/feasible_sets/instances_with_changes_in_batch_size_set.json", "w") as f:
    #     json.dump({
    #         "dataset_name": "instances_with_changes_in_batch_size_set",
    #         "instances": [instance.to_dict() for instance in instances]
    #     }, f, indent=4)


def parse_data_set(file_name):
    """
    Given a file path containing a dataset, parse it to a list of ParsedInstance objects for further processing.
    :param file_name: str for the file path to the dataset file.
    :return: list of ParsedInstance objects.
    """
    # Open dataset file.
    f = open(file_name)

    # Parse data.
    data = json.load(f)
    f.close()

    instance_list: list[ParsedInstance] = []
    for instance_info in data["instances"]:
        # Create a ParsedInstance object for each problem instance in the dataset.
        instance_list.append(ParsedInstance(instance_info))

    return instance_list, data["dataset_name"]
