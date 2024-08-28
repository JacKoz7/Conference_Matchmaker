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
            attr_list[i : i + self.n_recommendations]
            for i in range(0, len(attr_list), self.n_recommendations)
        ]
        return grouped_list

    def return_recommended_desired_attributes(
        self, solution: Dict[int, List[int]]
    ) -> List:
        return [self.participant_map[id]["desired"] for id in solution.keys()]

    def fitness_function(self, solution: Dict[int, List[int]]) -> float:
        """
        Calculate the fitness score for a given solution.

        This function evaluates the quality of matches for each participant in the solution.
        It considers various factors to determine the overall fitness:

        1. Match quality: How well the attributes of matched participants align with desired attributes.
        2. Early good matches: Bonus for good matches appearing earlier in the recommendation list.
        3. Self-recommendation penalty: Penalizes solutions where a participant is recommended to themselves.
        4. No matches penalty: Penalizes when a participant has no matching attributes with their recommendations.
        5. Attribute diversity bonus: Rewards solutions that provide diverse attribute matches.

        Args:
            solution (Dict[int, List[int]]): A dictionary where keys are participant IDs and values are lists of recommended participant IDs.

        Returns:
            float: The normalized fitness score for the given solution.
        """
        score = 0.0

        for p_id, p_matches in solution.items():
            participant_score = 0.0
            desired_attrs = set(self.participant_map[p_id]["desired"])

            # Penalty for self-recommendation
            if p_id in p_matches:
                participant_score -= 1.0

            matched_attrs = set()
            for i, match in enumerate(p_matches):
                match_attrs = set(self.participant_map[match]["attributes"])
                matched_attrs.update(match_attrs)

                # Score based on match quality
                attr_match_count = len(match_attrs & desired_attrs)
                participant_score += attr_match_count / len(desired_attrs)

                # Bonus for early good matches
                participant_score += attr_match_count / ((i + 1) * len(desired_attrs))

            # Penalty for no matches
            if len(matched_attrs & desired_attrs) == 0:
                participant_score -= 2.0
            # Bonus for attribute diversity
            diversity_score = len(matched_attrs & desired_attrs) / len(desired_attrs)
            participant_score += diversity_score

            score += participant_score

        # Normalize score by number of participants
        return score / len(solution)

    def run(
        self,
        generations: int,
        max_iterations_without_improvement: int,
        log_interval: int = 100,
    ) -> Dict[int, List[int]]:
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

            if i % log_interval == 0:
                print(f"iteration: {i:5d}\tscore: {best_score:.3f}")

            if (
                len(last_scores) == max_iterations_without_improvement
                and len(set(last_scores)) == 1
            ):
                print(
                    f"\n(no improvement for the last {max_iterations_without_improvement} iterations. stopping)\n"
                )
                break

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
