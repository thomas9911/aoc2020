from __future__ import annotations
import re

from typing import NamedTuple, Optional


class PassportExecption(Exception):
    def __init__(self, fields, original_exception):
        self.fields = fields
        self.original_exception = original_exception

    def __str__(self):
        return str(self.original_exception)


class Passport(NamedTuple):
    byr: int
    iyr: int
    eyr: int
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[str] = None

    @staticmethod
    def cast(kwargs):
        lookup = {k: make_validation_function(k) for k in Passport._fields}

        cast_data = {}
        for (key, value) in kwargs.items():
            try:
                new_value = lookup[key](value)
                cast_data[key] = new_value
            except ValueError:
                continue

        return cast_data

    @staticmethod
    def parse(input: str) -> Passport:
        args = input.split()
        fields = [x.split(":") for x in args]
        data = dict(fields)

        try:
            data = Passport.cast(data)
            return Passport(**data)
        except TypeError as e:
            raise PassportExecption(dict(fields), e) from None


def valid_birth_year(year):
    year = int(year)
    if 1920 <= year <= 2002:
        return year
    raise ValueError


def valid_issue_year(year):
    year = int(year)
    if 2010 <= year <= 2020:
        return year
    raise ValueError


def valid_expiration_year(year):
    year = int(year)
    if 2020 <= year <= 2030:
        return year
    raise ValueError


def valid_height(height):
    if height.endswith("cm"):
        parsed_height = int(height.replace("cm", "", 1))
        if 150 <= parsed_height <= 193:
            return parsed_height
    if height.endswith("in"):
        parsed_height = int(height.replace("in", "", 1))
        if 59 <= parsed_height <= 76:
            return parsed_height
    raise ValueError


def valid_color(color):
    prog = re.compile("^#[a-f0-9]{6}$")
    if re.fullmatch(prog, color):
        return color
    raise ValueError


def valid_eye_color(color):
    if color in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return color
    raise ValueError


def valid_passport_id(pid):
    if len(pid) == 9 and pid.isdigit():
        return pid
    raise ValueError


def valid_country_id(id):
    return id


def make_validation_function(key):
    if key == "byr":
        return valid_birth_year
    if key == "iyr":
        return valid_issue_year
    if key == "eyr":
        return valid_expiration_year
    if key == "hgt":
        return valid_height
    if key == "hcl":
        return valid_color
    if key == "ecl":
        return valid_eye_color
    if key == "pid":
        return valid_passport_id
    if key == "cid":
        return valid_country_id
    raise KeyError


with open("data.txt", "r") as f:
    data = f.read().split("\n\n")
    data = [x.replace("\n", " ") for x in data]

    count_valid = 0

    for item in data:
        try:
            passport = Passport.parse(item)
            print(passport)
            count_valid += 1

        except PassportExecption as e:
            # data = e.fields
            # print(e)
            # print(data)
            pass

    print(count_valid)
