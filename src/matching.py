import random
from typing import Dict, List
from collections import deque


class Algorithm:
    def __init__(
            self, participant_map: Dict[int, Dict[str, List[str]]], n_recommendations: int
    ):
        self.participant_map = participant_map
        self.n_recommendations = n_recommendations
        self.solution = self.random_solution()

    def random_solution(self) -> Dict[int, List[int]]:
        all_ids = list(self.participant_map.keys())
        random.shuffle(all_ids)

        solution = {}
        for p_id in self.participant_map:
            solution[p_id] = random.sample(all_ids, self.n_recommendations)

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

    def return_recommended_desired_attributes(
            self, solution: Dict[int, List[int]]
    ) -> List:
        return [self.participant_map[id]["desired"] for id in solution.keys()]

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

    def run(self, generations: int, max_iterations_without_improvement: int) -> Dict[int, List[int]]:
        best_solution = self.solution
        best_score = self.fitness_function(best_solution)
        last_scores = deque(maxlen=max_iterations_without_improvement)

        for i in range(generations):
            new_solution = self.mutate()
            new_score = self.fitness_function(new_solution)

            if new_score > best_score:
                best_solution = new_solution
                best_score = new_score
                self.solution = new_solution

            last_scores.append(best_score)

            if i % 50 == 0:  # wyświetla wynik co 50 iteracji
                print(f" score: {best_score} iteration {i}")

            # Sprawdza, czy wszystkie wyniki w deque są takie same
            if len(last_scores) == max_iterations_without_improvement and len(set(last_scores)) == 1:
                print(f"\nNo improvement for the last {max_iterations_without_improvement} iterations. Stopping.")
                break

        print(f"\nFinal result: {best_score}\n")
        return best_solution

    def mutate(self) -> Dict[int, List[int]]:
        mutated_solution = self.solution.copy()
        all_ids = list(self.participant_map.keys())

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
