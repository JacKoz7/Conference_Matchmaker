def print_solution(algorithm, solution) -> None:
    for ids in range(len(algorithm.give_desired_attributes(solution))):
        print(
            f"Participant {ids+1} desired attributes: {algorithm.give_desired_attributes(solution)[ids]}"
        )
    print()

    for ids in range(len(algorithm.give_attributes(solution))):
        print(
            f"Attributes of participants matched for Participant {ids+1}: {algorithm.give_attributes(solution)[ids]}"
        )
    print()

    for points in range(len(algorithm.find_matches(solution))):
        print(f"Participant {points+1} matches: {algorithm.find_matches(solution)[points]}")
    print()

    for index, ids in enumerate(solution.values()):
        participants_ids = ", ".join(map(str, ids))
        print(
            f"Participant number {index + 1} matched with participants with IDs {participants_ids}"
        )
