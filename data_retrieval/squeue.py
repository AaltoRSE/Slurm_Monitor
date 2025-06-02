import re
import os
from typing import Dict
from data_retrieval.utils import run_command


class SQUEUE:
    def __init__(self):
        job_data = parse_squeue_output()
        self.pending_data = {
            job["ID"].split("_")[0]: {
                "start": job["Start"],
                "nodes": job["Nodes"],
                "state": job["State"],
            }
            for job in job_data
            if job["State"] == "PENDING"
        }
        self.running_data = {
            job["ID"].split("_")[0]: {
                "start": job["Start"],
                "nodes": job["NodeList"],
                "state": job["State"],
            }
            for job in job_data
            if job["State"] == "RUNNING"
        }

    def get_start_time(self, id):
        queue_id = id.split("_")[0]
        return (
            self.pending_data[queue_id]["start"]
            if queue_id in self.pending_data
            else None
        )

    def get_nodes(self, id):
        queue_id = id.split("_")[0]
        alloc_nodes = (
            self.running_data[queue_id] if queue_id in self.running_data else None
        )
        expected_nodes = (
            self.pending_data[queue_id] if queue_id in self.pending_data else None
        )
        return alloc_nodes, expected_nodes

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.data


def parse_squeue_output() -> Dict[str, str]:
    """
    Parses the SQUEUE output to extract Scheduled Nodes and Expected Start Time.

    Args:
        output (str): The SQUEUE command output as a string.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing (Scheduled Nodes, Expected Start Time).
    """
    output = run_command(
        f"squeue -u {os.environ.get('USER')} -O JobID:20,StartTime:20,SchedNodes:50,State:20,NodeList:200"
    )
    results = []
    lines = output.strip().split("\n")
    for line in lines[1:]:
        # Match the expected format
        match = re.search(
            r"(?P<ID>\S+)\s+(?P<Start>\S)+\s+(?P<Nodes>\S)+\s+(?P<State>\S)+\s+(?P<NodeList>\S)+\s",
            line,
        )
        if match:
            results.append(match.groupdict())
    return results
