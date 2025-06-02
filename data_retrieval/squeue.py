import re
import os
from typing import Dict
from data_retrieval.utils import run_command


class SQUEUE:
    def __init__(self):
        self.data = {
            job["ID"].split("_")[0]: {
                "start": job["Start"],
                "nodes": job["Nodes"],
                "state": job["State"],
            }
            for job in parse_squeue_output()
            if job["State"] == "PENDING"
        }

    def get_start_time(self, id):
        queue_id = id.split("_")[0]
        return self.data[queue_id]["start"] if queue_id in self.data else None

    def get_nodes(self, id):
        queue_id = id.split("_")[0]
        return self.data[queue_id]["nodes"] if queue_id in self.data else "unknown"

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
        f"squeue -u {os.environ.get('USER')} -O JobID:20,StartTime:20,SchedNodes:50"
    )
    results = []
    lines = output.strip().split("\n")
    for line in lines[1:]:
        # Match the expected format
        match = re.search(
            r"(?P<ID>\S+)\s+(?P<Start>\S)+\s+(?P<Nodes>\S)+\s+(?P<State>\S)+\s", line
        )
        if match:
            results.append(match.groupdict())
    return results
