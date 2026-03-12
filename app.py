
import sys
import os
# Necessary for relative file loading
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Use the configurable logger
from logger import get_logger
from flask import Flask, send_from_directory, jsonify
from data_retrieval import data_retrieval, quotas


logger = get_logger()

monitor_app = Flask(
    "Example OOD app", static_folder="frontend/dist", static_url_path=""
)

# Serve the Vue.js frontend
@monitor_app.route("/")
def serve_frontend():
    return send_from_directory(monitor_app.static_folder, "index.html")


@monitor_app.route("/api/running_jobs")
def get_current_jobs():
    try:
        return jsonify([data.model_dump() for data in data_retrieval.fetch_running_jobs()])
    except Exception as e:
        logger.exception(f"Error fetching running jobs: {e}")
        return jsonify({"error": "Failed to fetch running jobs"}), 500


@monitor_app.route("/api/finished_jobs")
def get_finished_jobs():
    try:
        return jsonify([data.model_dump() for data in data_retrieval.fetch_finished_jobs()])
    except Exception as e:
        logger.exception(f"Error fetching finished jobs: {e}")    
        return jsonify({"error": "Failed to fetch finished jobs"}), 500


@monitor_app.route("/api/quotas")
def get_quotas():
    try:
        return jsonify([data.model_dump() for data in quotas.get_quotas()])
    except Exception as e:
        logger.exception(f"Error fetching quotas: {e}")
        return jsonify({"error": "Failed to fetch quotas"}), 500

@monitor_app.route("/api/gpu_data/<int:job_id>")
def get_gpu_data(job_id: int):
    try:
        return jsonify(data_retrieval.fetch_gpu_graphs(job_id).model_dump())
    except Exception as e:
        logger.exception(f"Error fetching GPU data for job {job_id}: {e}")
        return jsonify({"error": "Failed to fetch GPU data"}), 500

# Serve other static files (e.g., JS, CSS)
@monitor_app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(monitor_app.static_folder, path)

if __name__ == "__main__":
    try:
        logger.info("Starting monitor app.")
        monitor_app.run()
    except Exception as e:
        logger.error(e)
