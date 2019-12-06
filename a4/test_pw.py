from .pw import is_valid, is_valid_part2, pw_candidates, input_range


def test_is_valid():
    assert is_valid(111111, (100000, 999999))
    assert is_valid(223456, input_range)
    assert not is_valid(223450, input_range)
    assert is_valid(123788, (100000, 999999))
    assert not is_valid(123789, input_range)
    assert not is_valid(999999, input_range)


def test_pw_candidates():
    assert list(pw_candidates((111111, 111122))) == [
        111111,
        111112,
        111113,
        111114,
        111115,
        111116,
        111117,
        111118,
        111119,
        111122,
    ]
    assert len(pw_candidates((111111, 111122))) == 10


def test_is_valid_part2():
    assert is_valid_part2(112233, (100000, 999999))
    assert not is_valid_part2(123444, (100000, 999999))
    assert is_valid_part2(111122, (100000, 999999))
