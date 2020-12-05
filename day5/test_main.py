from main import parse, gen_seat_id


def test_one():
    input = "FBFBBFFRLR"
    (row, column) = parse(input)
    assert row == 44
    assert column == 5
    assert 357 == gen_seat_id(row, column)


def test_two():
    input = "BFFFBBFRRR"
    (row, column) = parse(input)
    assert row == 70
    assert column == 7
    assert 567 == gen_seat_id(row, column)


def test_three():
    input = "FFFBBBFRRR"
    (row, column) = parse(input)
    assert row == 14
    assert column == 7
    assert 119 == gen_seat_id(row, column)


def test_four():
    input = "BBFFBBFRLL"
    (row, column) = parse(input)
    assert row == 102
    assert column == 4
    assert 820 == gen_seat_id(row, column)
