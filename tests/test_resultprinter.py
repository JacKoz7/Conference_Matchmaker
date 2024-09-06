from src.resultprinter import print_solution
import pytest


@pytest.fixture
def example_solution() -> dict:
    return {
        1: [2, 3],
        2: [3, 4],
        3: [1, 4],
        4: [1, 2],
    }


def test_print_solution_output(capfd, example_solution):
    print_solution(example_solution)

    captured = capfd.readouterr()

    expected_output = (
        "Participant 1 matched with 2, 3\n"
        "Participant 2 matched with 3, 4\n"
        "Participant 3 matched with 1, 4\n"
        "Participant 4 matched with 1, 2\n"
    )

    assert captured.out == expected_output


def test_print_empty_solution(capfd):
    print_solution({})

    captured = capfd.readouterr()

    assert captured.out == ""
