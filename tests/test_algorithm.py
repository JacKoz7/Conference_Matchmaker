import pytest
from src.matching import Algorithm
from typing import Dict, List


@pytest.fixture
def sample_participant_map() -> Dict[int, Dict[str, List[str]]]:
    return {
        1: {"attributes": ["attr1", "attr2"], "desired": ["desired1", "desired2"]},
        2: {"attributes": ["attr3", "attr4"], "desired": ["desired3", "desired4"]},
        3: {"attributes": ["attr5", "attr6"], "desired": ["desired5", "desired6"]},
        4: {"attributes": ["attr7", "attr8"], "desired": ["desired7", "desired8"]},
    }


@pytest.fixture
def algorithm(sample_participant_map):
    return Algorithm(sample_participant_map, n_recommendations=2)


def test_random_solution(algorithm):
    solution = algorithm.random_solution()
    assert len(solution) == 4
    for recommendations in solution.values():
        assert len(recommendations) == 2
        assert len(set(recommendations)) == 2  # No duplicates
        assert all(1 <= id <= 4 for id in recommendations)  # Valid IDs


def test_return_participants_attributes(algorithm):
    solution = {1: [2, 3], 2: [3, 4], 3: [1, 4], 4: [1, 2]}
    attrs = algorithm.return_participants_attributes(solution)
    assert len(attrs) == 4
    assert all(len(group) == 2 for group in attrs)
    assert attrs[0] == [["attr3", "attr4"], ["attr5", "attr6"]]


def test_return_recommended_desired_attributes(algorithm):
    solution = {1: [2, 3], 2: [3, 4], 3: [1, 4], 4: [1, 2]}
    desired = algorithm.return_recommended_desired_attributes(solution)
    assert len(desired) == 4
    assert desired == [
        ["desired1", "desired2"],
        ["desired3", "desired4"],
        ["desired5", "desired6"],
        ["desired7", "desired8"],
    ]


def test_fitness_function(algorithm):
    solution = {1: [2, 3], 2: [3, 4], 3: [1, 4], 4: [1, 2]}
    fitness = algorithm.fitness_function(solution)
    assert isinstance(fitness, float)


def test_run(algorithm):
    solution = algorithm.run(generations=100, max_iterations_without_improvement=10)
    assert isinstance(solution, dict)
    assert len(solution) == 4
    for recommendations in solution.values():
        assert len(recommendations) == 2
        assert len(set(recommendations)) == 2
        assert all(1 <= id <= 4 for id in recommendations)


def test_run_early_stop(algorithm):
    solution = algorithm.run(generations=1000, max_iterations_without_improvement=5)
    assert isinstance(solution, dict)
    assert len(solution) == 4

# brak test_mutate() :(