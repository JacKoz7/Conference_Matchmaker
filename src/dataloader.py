from typing import Dict, List


def load_from_file(input_file: str) -> Dict[int, Dict[str, List[str]]]:
    participants = {}
    with open(input_file, "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            participant_id = int(parts[0])
            attributes = parts[1].split(",")
            desired_attributes = parts[2].split(",")
            participants[participant_id] = {
                "attributes": attributes,
                "desired": desired_attributes,
            }
    return participants
