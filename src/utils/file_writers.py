import json
import logging
import os


def write_perturbed_instance_to_file(perturbed_instance, nominal_instance_id, perturbation_stats):
    """
    Write a perturbed problem instance to a json file.
    :param perturbed_instance: ParsedInstance | CustomInstance | ProblemInstance  object.
    :param nominal_instance_id: id of the instance that was perturbed.
    :param perturbation_stats: Dictionary containing stats about the perturbation.
    """

    # Check if directory is present
    if not os.path.exists(f"data/perturbed_instances/{nominal_instance_id}"):
        os.makedirs(f"data/perturbed_instances/{nominal_instance_id}")

    perturbation_id = perturbation_stats["perturbation_id"]
    file_path = f"data/perturbed_instances/{nominal_instance_id}/{perturbation_id}.json"

    try:
        with open(file_path, "w") as f:
            json.dump({
                "perturbed_id": perturbation_id,
                "nominal_instance": nominal_instance_id,
                "gamma": perturbation_stats["gamma"],
                "epsilon": perturbation_stats["epsilon"],
                "number_of_perturbed_jobs": perturbation_stats["number_of_perturbed_jobs"],
                "number_of_job_augmentations": perturbation_stats["number_of_job_augmentations"],
                "number_of_jobs_decreases": perturbation_stats["number_of_jobs_decreases"],
                "batch_augmentation_is_required": perturbation_stats["batch_augmentation_is_required"],
                "instance": perturbed_instance.to_dict(),
            }, f, indent=4)
        logging.info(f"Successfully created json file: {file_path}")

    except:
        logging.error(f"Failed to create json file, please try again")
        return


def write_instance_to_file(instance, instance_name: str, file_path: str):
    """
    Write problem instance to a json file.
    :param instance: ParsedInstance | CustomInstance | ProblemInstance  object.
    :param instance_name: Specified name for the instance.
    :param file_path: Specified path where file will be created.
    """
    try:
        with open(file_path, "w") as f:
            json.dump({
                "instance_name": f"{instance_name}",
                "instance": instance.to_dict()
            }, f, indent=4)
        logging.info(f"Successfully created json file: {file_path}")

    except:
        logging.error(f"Failed to create json file, please try again")
        return


def write_dataset_to_file(instances, dataset_name: str, file_path: str):
    """
    Write dataset to a json file.
    :param instances: list[ParsedInstance | CustomInstance | ProblemInstance]  object.
    :param dataset_name: Specified name for the dataset.
    :param file_path: Specified path where file will be created.
    """
    try:
        with open(file_path, "w") as f:
            json.dump({
                "dataset_name": f"{dataset_name}",
                "instances": [instance.to_dict() for instance in instances]
            }, f, indent=4)
        logging.info(f"Successfully created data set file: {file_path}")

    except:
        logging.error("Failed to create json file, try again.")
        return


def write_results_to_file(analysis_type, method, file_name, results):
    """
    Write results produced by a script to json file.
    :param analysis_type: str specifying the type of analysis performed.
    :param method: str specifying the type of method used.
    :param file_name: str specifying the name of the file to be created.
    :param results: dictionary object containing the results.
    """
    if not os.path.exists(f"data/results/{analysis_type}"):
        os.makedirs(f"data/results/{analysis_type}")
    if not os.path.exists(f"data/results/{analysis_type}/{method}"):
        os.makedirs(f"data/results/{analysis_type}/{method}")
    try:
        path = f"data/results/{analysis_type}/{method}/results_{file_name}.json"
        with open(path, "w") as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results recorded successfully: {path}")

    except:
        logging.error("Failed to create json file with results")
        return
