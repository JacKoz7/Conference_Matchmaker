from matching import Algorithm


def print_solution(participants, solution) -> None:
    algorithm = Algorithm(participants)
    for ids in range(len(algorithm.return_recommended_desired_attributes(solution))):
        print(
            f"Participant {ids + 1} desired attributes: {algorithm.return_recommended_desired_attributes(solution)[ids]}"
        )
    print()

    for ids in range(len(algorithm.return_participants_attributes(solution))):
        print(
            f"Attributes of participants matched with Participant {ids + 1}: {algorithm.return_participants_attributes(solution)[ids]}"
        )
    print()

    for points in range(len(algorithm.find_matches(solution))):
        print(f"Participant {points + 1} matches: {algorithm.find_matches(solution)[points]}")
    print()

    for index, ids in enumerate(solution.values()):
        participants_ids = ", ".join(map(str, ids))
        print(
            f"Participant number {index + 1} matched with participants with IDs {participants_ids}"
        )
