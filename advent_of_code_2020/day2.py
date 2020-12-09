import typing
from collections import namedtuple
from pprint import pprint

from .data_tools import read_input

PolicyPass = namedtuple('PolicyPass', ['min', 'max', 'letter', 'password'])


def parse_policy_password(line: str) -> PolicyPass:
    policy, password = line.split(': ')
    num_range, letter = policy.split()
    low, high = map(int, num_range.split('-'))
    return PolicyPass(min=low, max=high, letter=letter, password=password)


def parse_input(data: str) -> typing.List[PolicyPass]:
    lines = [parse_policy_password(l) for l in data.splitlines()]
    return lines


def filter_valid_records1(records: typing.List[PolicyPass]) -> typing.List[PolicyPass]:
    '''Part 1
    '''
    filtered_records = []

    for rec in records:
        count = rec.password.count(rec.letter)
        if rec.min <= count <= rec.max:
            filtered_records.append(rec)
    
    return filtered_records


def filter_valid_records2(records: typing.List[PolicyPass]) -> typing.List[PolicyPass]:
    '''Part 1
    '''
    filtered_records = []

    for rec in records:
        a, b = rec.password[rec.min - 1] == rec.letter, rec.password[rec.max - 1] == rec.letter
        if (a + b) == 1:
            filtered_records.append(rec)
    
    return filtered_records


def main(input_data_path: str):
    raw_data = read_input(input_data_path)
    records = parse_input(raw_data)
    filtered_recs1 = filter_valid_records1(records)
    filtered_records2 = filter_valid_records2(records)

    print(f'Number of valid records (v1): {len(filtered_recs1)}')
    print(f'Number of valid records (v2): {len(filtered_records2)}')
