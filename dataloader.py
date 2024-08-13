from typing import List
from participantdata import Participant


def load_from_file(input_file: str) -> List[Participant]:
    participants = []
    with open(input_file, "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            participant_id = int(parts[0])
            attributes = parts[1].split(",")
            desired_attributes = parts[2].split(",")
            participant = Participant(participant_id, attributes, desired_attributes)
            participants.append(participant)
    return participants
