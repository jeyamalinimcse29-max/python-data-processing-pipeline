from reader import read_data
from cleaner import clean_data
from transformer import transform_data
from logger import logger
import csv
import json
import os


base_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_file = os.path.join(base_folder, "config", "config.json")

with open(config_file, "r") as file:
    config = json.load(file)


input_file = os.path.join(base_folder, config["input_file"])
output_file = os.path.join(base_folder, config["output_file"])


def run_pipeline():

    logger.info("Pipeline started")

    data = read_data(input_file)
    logger.info("Data read successfully")

    cleaned_data = clean_data(data)
    logger.info("Data cleaned successfully")

    transformed_data = transform_data(cleaned_data)
    logger.info("Data transformed successfully")

    with open(output_file, "w", newline="") as file:

        fieldnames = transformed_data[0].keys()

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(transformed_data)

    logger.info("Output file created successfully")
    logger.info("Pipeline completed")

    print("Pipeline completed successfully")
    print("Output file:", output_file)
    return output_file


if __name__ == "__main__":
    run_pipeline()