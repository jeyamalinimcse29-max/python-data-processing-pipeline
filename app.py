import os
import sys
import json
import csv
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

# Add src to path for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from reader import read_data
from cleaner import clean_data
from transformer import transform_data
from logger import logger

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "frontend"), static_url_path="")
CORS(app)

CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

INPUT_FILE = os.path.join(BASE_DIR, config["input_file"])
OUTPUT_FILE = os.path.join(BASE_DIR, config["output_file"])
LOG_FILE = os.path.join(BASE_DIR, "logs", "pipeline.log")

def run_pipeline_internal():
    logger.info("Pipeline started via API")
    data = read_data(INPUT_FILE)
    logger.info("Data read successfully")
    cleaned_data = clean_data(data)
    logger.info("Data cleaned successfully")
    transformed_data = transform_data(cleaned_data)
    logger.info("Data transformed successfully")
    with open(OUTPUT_FILE, "w", newline="") as file:
        if transformed_data:
            fieldnames = transformed_data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transformed_data)
    logger.info("Output file created successfully")
    logger.info("Pipeline completed")
    return True

def read_csv_as_list(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    # Convert numeric strings where possible
    return rows

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/run", methods=["POST"])
def api_run():
    try:
        run_pipeline_internal()
        return jsonify({"status": "success", "message": "Pipeline completed successfully"}), 200
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/input", methods=["GET"])
def api_input():
    data = read_csv_as_list(INPUT_FILE)
    return jsonify(data)

@app.route("/api/output", methods=["GET"])
def api_output():
    data = read_csv_as_list(OUTPUT_FILE)
    return jsonify(data)

@app.route("/api/logs", methods=["GET"])
def api_logs():
    if not os.path.exists(LOG_FILE):
        return jsonify({"logs": ""})
    with open(LOG_FILE, "r") as f:
        logs = f.read()
    # Return last 500 lines
    lines = logs.splitlines()
    tail = "\n".join(lines[-500:])
    return jsonify({"logs": tail})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
