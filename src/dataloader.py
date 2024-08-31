from typing import Dict, List


class Dataloader:

    def __init__(self, input_file: str):
        self.input_file = input_file

    def load_from_file(self) -> Dict[int, Dict[str, List[str]]]:
        participants = {}
        with open(self.input_file, "r") as file:
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

    def count_participants(self) -> int:
        with open(self.input_file, "r") as file:
            return sum(1 for line in file)
