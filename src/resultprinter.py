def print_solution(solution) -> None:
    for index, ids in enumerate(solution.values()):
        participants_ids = ", ".join(map(str, ids))
        print(
            f"Participant number {index + 1} matched with participants with IDs {participants_ids}"
        )
