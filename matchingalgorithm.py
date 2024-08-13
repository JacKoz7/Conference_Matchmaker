import random
from typing import Dict, List
from participantdata import Participant


class Algorithm:
    def __init__(self, participants: list[Participant], n_recommendations: int = 5):
        self.participants = participants
        self.participant_map = self.convert_participants_to_map()
        self.n_recommendations = n_recommendations
        self.solution = self.random_solution()

    def random_solution(self) -> Dict[int, List[int]]:
        all_ids = [p.id for p in self.participants]
        random.shuffle(all_ids)

        solution = {}
        for p in self.participants:
            solution[p.id] = random.sample(all_ids, self.n_recommendations)

        return solution

    def give_attributes(self, solution: Dict[int, List[int]]) -> List:
        attr_list = []
        for matches in solution.values():
            for i in matches:
                attr_list.append(self.participant_map[i]["attributes"])
        grouped_list = [
            attr_list[i : i + self.n_recommendations]
            for i in range(0, len(attr_list), self.n_recommendations)
        ]
        return grouped_list

    def give_desired_attributes(self, solution: Dict[int, List[int]]) -> List:
        des_list = []
        for id in solution.keys():
            des_list.append(self.participant_map[id]["desired"])
        return des_list

    def find_matches(self, solution: Dict[int, List[int]]) -> List:
        attributes = self.give_attributes(solution)
        desired_attributes = self.give_desired_attributes(solution)
        match_counts = []
        for attr_group, desired_attr_group in zip(attributes, desired_attributes):
            group_match_counts = []
            for attr_list in attr_group:
                count = sum(1 for attr in attr_list if attr in desired_attr_group)
                group_match_counts.append(count)
            match_counts.append(group_match_counts)
        return match_counts

    def fitness_function(self, solution: Dict[int, List[int]]):
        score = 0
        for p_id, p_matches in solution.items():
            # R1 rekomendacja dla samego siebie
            if p_id in p_matches:
                score -= 100

        for i in range(len(self.find_matches(solution))):
            # R2 Brak dopasowań wśród 5 osób
            if sum(self.find_matches(solution)[i]) == 0:
                score -= 300
            for j in range(len(self.find_matches(solution)[i])):
                # R3 dopasowanie jednej cechy
                if self.find_matches(solution)[i][j] == 1:
                    score += 100
                # R4 dopasowanie dwóch cech
                if self.find_matches(solution)[i][j] == 2:
                    score += 200
                # R5 dopasowanie trzech lub więcej cech
                if self.find_matches(solution)[i][j] >= 3:
                    score += 300

        return score

    def convert_participants_to_map(self):
        participants_map = {}
        for p in self.participants:
            participants_map[p.id] = {
                "attributes": p.attributes,
                "desired": p.desired_attributes,
            }
        return participants_map

    def run(self, generations: int) -> Dict[int, List[int]]:
        for i in range(0, generations):
            new_solution = self.mutate(self.solution)

            if self.fitness_function(new_solution) > self.fitness_function(
                self.solution
            ):
                self.solution = new_solution
        print("score: ", self.fitness_function(self.solution), "\n")
        return self.solution

    def mutate(self, solution: Dict[int, List[int]]) -> Dict[int, List[int]]:
        new_solution = {}
        all_ids = [p.id for p in self.participants]

        for participant_id in solution.keys():
            possible_recommendations = [pid for pid in all_ids]
            new_solution[participant_id] = random.sample(
                possible_recommendations, self.n_recommendations
            )

        return new_solution
