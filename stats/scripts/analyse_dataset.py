import argparse
import json
import logging
import os

# Set log level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Parse script arguments
parser = argparse.ArgumentParser(description="Script to produce stats for dataset")

parser.add_argument("--file", help="Specify file path to dataset file.")

args = parser.parse_args()


def analyse_dataset(file: str):
    try:
        with open(file) as json_file:
            data = json.load(json_file)
            instances = data["instances"]
            dataset_name = data["dataset_name"]
            # Record Number of problem instances
            # Record Average job processing time
            # Record Average number of jobs per instance
            # Record Average number of timeslots per instance
            # Record Average batch size

            average_processing = 0
            total_number_of_jobs = 0
            total_batch_size = 0
            total_number_of_timeslots = 0
            for instance in instances:
                total_pressing_time = 0
                jobs = instance["jobs"]
                for job in jobs:
                    total_pressing_time = total_pressing_time + job["processing_time"]

                total_number_of_jobs = total_number_of_jobs + instance["number_of_jobs"]
                total_batch_size = total_batch_size + instance["G"]
                total_number_of_timeslots = total_number_of_timeslots + instance["T"]
                average_processing = average_processing + (total_pressing_time / len(jobs))

            stats = {
                "dataset_name": dataset_name,
                "Number-of-instances": len(instances),
                "Average-job-processing-time": average_processing / len(instances),
                "Average-number-of-jobs-per-instance": total_number_of_jobs / len(instances),
                "Average-batch-size-per-instance": total_batch_size / len(instances),
                "Average-number-of-timeslots-per-instance": total_number_of_timeslots / len(instances)
            }

            # Check if directory is present
            if not os.path.exists('data/dataset_stats'):
                os.makedirs('data/dataset_stats')
            try:
                path = f"data/dataset_stats/{dataset_name}_stats.json"
                with open(path, "w") as f:
                    json.dump(stats, f, indent=4)
                logging.info(f"Successfully created data set file: {path}")

            except:
                logging.error("Failed to create json file, try again.")
                return
            logging.info(f"Successfully loaded json file: {file}")


    except:
        logging.error(f"Failed to parse json, please try again: {file}")
        return


analyse_dataset(args.file)
