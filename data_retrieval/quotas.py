import re
import os
from typing import List
from data_retrieval.utils import run_command
from models.models import Quota

user_quotas = re.compile(
    r" *\/(?P<name>\w+) +(\(user qta\) +)?(?P<used>\d+\w) +(?P<available>\d+\w) +(\d+\w)[ -]+(?P<used_files>\d+\w?) +(?P<files>\d+\w?) +(\d+\w?) +"
)

group_quotas = re.compile(
    r" *\/(\w+) +(?P<name>\w+) +(?P<used>\d+\w) +(?P<available>\d+\w) +(\d+\w)[ -]+(?P<used_files>\d+\w?) +(?P<files>\d+\w?) +(\d+\w?) +"
)


def parse_file_count(filecount: str):
    if filecount.endswith("k"):
        return int(filecount[:-1]) * 1000
    else:
        return int(filecount)


def parse_storage(storage_string):
    conversion_factors = {"K": 1e3, "M": 1e6, "G": 1e9, "T": 1e12}
    suffix = storage_string[-1]
    try:
        factor = conversion_factors[suffix]
        return int(storage_string[:-1]) * factor

    except:
        try:
            return int(storage_string)
        except:
            raise ValueError("Invalid space value")


def convert_quota_dict_to_quota(quota_dict, path, name):
    return Quota(
        name=name,
        path=path,
        used=parse_storage(quota_dict["used"]),
        total=parse_storage(quota_dict["available"]),
        used_files=parse_file_count(quota_dict["used_files"]),
        files=parse_file_count(quota_dict["files"]),
    )


def get_quotas() -> List[Quota]:
    """
    Parses the SQUEUE output to extract Scheduled Nodes and Expected Start Time.

    Args:
        output (str): The SQUEUE command output as a string.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing (Scheduled Nodes, Expected Start Time).
    """
    output = run_command("/usr/local/bin/quota")
    results = []
    lines = output.strip().split("\n")
    username = os.environ.get("USER")

    for line in lines[1:]:
        # Match the expected format
        home_match = re.search(user_quotas, line)
        if not home_match is None:
            print(home_match)
            group_dict = home_match.groupdict()
            if group_dict["name"] == "home":
                results.append(
                    convert_quota_dict_to_quota(
                        group_dict, path=f"/home/{username}", name="Home"
                    )
                )
            else:
                results.append(
                    convert_quota_dict_to_quota(
                        group_dict, path=f"/scratch/work/{username}", name="Work"
                    )
                )
        group_match = re.search(group_quotas, line)
        if not group_match is None:
            group_dict = group_match.groupdict()
        if not group_match is None:
            group_dict = group_match.groupdict()
            if group_dict["name"] != username:
                results.append(
                    convert_quota_dict_to_quota(
                        group_dict,
                        path=f"project folder on /scratch",
                        name=group_dict["name"],
                    )
                )

    return results
