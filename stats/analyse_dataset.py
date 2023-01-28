import argparse
import json
import logging

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

            
            logging.info(f"Successfully loaded json file: {file}")
    except:
        logging.error(f"Failed to parse json, please try again: {file}")
        return

analyse_dataset(args.file)