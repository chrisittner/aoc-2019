from typing import List

input_range = (165432, 707912)


def is_valid(pw_cand: int, inclusive_range: tuple) -> bool:
    is_6_digit = 100000 <= pw_cand <= 999999

    lower, upper = inclusive_range
    is_within_range = lower <= pw_cand <= upper

    digits = [int(digit) for digit in str(pw_cand)]
    two_adjacent_digits_same = any(
        [left == right for left, right in zip(digits, digits[1:])]
    )

    has_nondecreasing_digits = all(
        [left <= right for left, right in zip(digits, digits[1:])]
    )

    return (
        is_6_digit
        and is_within_range
        and two_adjacent_digits_same
        and has_nondecreasing_digits
    )


def is_valid_part2(pw_cand: int, inclusive_range: tuple) -> bool:
    digits = [int(digit) for digit in str(pw_cand)]
    d = digits
    two_adjacent_digits_same_not_part_in_larger_group = (
        (d[0] == d[1] and d[1] < d[2])
        or (d[0] < d[1] == d[2] and d[2] < d[3])
        or (d[1] < d[2] == d[3] and d[3] < d[4])
        or (d[2] < d[3] == d[4] and d[4] < d[5])
        or (d[3] < d[4] == d[5])
    )

    return (
        is_valid(pw_cand, inclusive_range)
        and two_adjacent_digits_same_not_part_in_larger_group
    )


def pw_candidates(inclusive_range: tuple, validator=is_valid) -> List[int]:
    return [
        pw_cand
        for pw_cand in range(inclusive_range[0], inclusive_range[1] + 1)
        if validator(pw_cand, inclusive_range)
    ]


if __name__ == "__main__":
    print(len(pw_candidates(input_range)))

    print(len(pw_candidates(input_range, is_valid_part2)))
