import json
import logging


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
