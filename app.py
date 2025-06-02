from flask import Flask, send_from_directory, jsonify
import subprocess
import data_retrieval.data_retrieval as data_retrieval
from data_retrieval import quotas

monitor_app = Flask("User Monitor", static_folder="frontend/dist", static_url_path="")


# Serve the Vue.js frontend
@monitor_app.route("/")
def serve_frontend():
    return send_from_directory(monitor_app.static_folder, "index.html")


@monitor_app.route("/api/running_jobs")
def get_current_jobs():
    return jsonify([data.model_dump() for data in data_retrieval.fetch_running_jobs()])


@monitor_app.route("/api/finished_jobs")
def get_current_jobs():
    return jsonify([data.model_dump() for data in data_retrieval.fetch_finished_jobs()])


@monitor_app.route("/api/quotas")
def get_current_jobs():
    return jsonify([data.model_dump() for data in quotas.get_quotas()])


# Serve other static files (e.g., JS, CSS)
@monitor_app.route("/<path:path>")
def serve_static_files(path):
    path = path.replace("..", "")
    return send_from_directory(monitor_app.static_folder, path)


if __name__ == "__main__":
    try:
        monitor_app.run()
    except Exception as e:
        print(e)
