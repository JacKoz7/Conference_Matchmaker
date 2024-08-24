import random
from typing import Dict, List
from participant import Participant


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

    def return_participants_attributes(self, solution: Dict[int, List[int]]) -> List:
        attr_list = []
        for matches in solution.values():
            for i in matches:
                attr_list.append(self.participant_map[i]["attributes"])
        grouped_list = [
            attr_list[i: i + self.n_recommendations]
            for i in range(0, len(attr_list), self.n_recommendations)
        ]
        return grouped_list

    def return_recommended_desired_attributes(self, solution: Dict[int, List[int]]) -> List:
        desired_list = []
        for id in solution.keys():
            desired_list.append(self.participant_map[id]["desired"])
        return desired_list

    def find_matches(self, solution: Dict[int, List[int]]) -> List:
        attributes = self.return_participants_attributes(solution)
        desired_attributes = self.return_recommended_desired_attributes(solution)
        match_counts = []
        for attr_group, desired_attr_group in zip(attributes, desired_attributes):
            group_match_counts = []
            for attr_list in attr_group:
                count = sum(1 for attr in attr_list if attr in desired_attr_group)
                group_match_counts.append(count)
            match_counts.append(group_match_counts)
        return match_counts

    def fitness_function(self, solution: Dict[int, List[int]]) -> int:
        score = 0

        # R1: Rekomendacja dla samego siebie
        for p_id, p_matches in solution.items():
            if p_id in p_matches:
                score -= 100

        # Wykonujemy znalezienie dopasowań tylko raz i zapisujemy
        match_results = self.find_matches(solution)

        # R2: Brak dopasowań wśród 5 osób
        for match_count in match_results:
            if sum(match_count) == 0:
                score -= 300

        # R3: Za każde dopasowanie 100 pkt
        for match_count in match_results:
            for count in match_count:
                score += count * 100

        # R4: Różnorodność preferencji (bonus za zróżnicowane spełnione preferencje)
        for p_id, p_matches in solution.items():
            desired_attrs = set(self.participant_map[p_id]["desired"])
            matched_attrs = set()
            for match in p_matches:
                matched_attrs.update(self.participant_map[match]["attributes"])
            if matched_attrs & desired_attrs:
                score += 50

        return score

    def convert_participants_to_map(self) :
        participants_map = {}
        for p in self.participants:
            participants_map[p.id] = {
                "attributes": p.attributes,
                "desired": p.desired_attributes,
            }
        return participants_map

    def run(self, generations: int) -> Dict[int, List[int]]:
        best_solution = self.solution
        best_score = self.fitness_function(best_solution)
        iterations_without_improvement = 0
        max_iterations_without_improvement = generations * 0.5  # 50% iteracji

        for i in range(generations):
            new_solution = self.mutate()
            new_score = self.fitness_function(new_solution)

            if new_score > best_score:
                best_solution = new_solution
                best_score = new_score
                self.solution = new_solution
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1

            print(f" score: {best_score} iteration {i}")

            # jeśli przez 50% wszystkich iteracji score będzie ciągle taki sam (nie będzie poprawy) to zakończ działanie
            if iterations_without_improvement >= max_iterations_without_improvement:
                print(f"\nNo improvement for {max_iterations_without_improvement} (50%) iterations. Stopping.")
                break

        print(f"\nFinal result: {best_score}\n")
        return best_solution

    def mutate(self) -> Dict[int, List[int]]:
        mutated_solution = self.solution.copy()
        all_ids = [p.id for p in self.participants]

        # Wybór losowo uczestnika do mutacji
        participant_to_mutate = random.choice(list(mutated_solution.keys()))

        # Wybór losowego indeksu do zmiany
        index_to_change = random.randint(0, self.n_recommendations - 1)

        # Wybór nowego uczestnika
        current_recommendations = set(mutated_solution[participant_to_mutate])
        new_recommendation = random.choice(
            [id for id in all_ids if id not in current_recommendations]
        )
        # Zmiana wybranej rekomendacji
        mutated_solution[participant_to_mutate][index_to_change] = new_recommendation

        return mutated_solution

