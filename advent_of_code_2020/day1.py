import typing
from collections import defaultdict

from .data_tools import read_input


def parse_data(input_string: str) -> typing.List[int]:
    return [int(s) for s in input_string.splitlines()]


def double_sum(data: typing.List[int]):
    numbers = defaultdict(lambda: None)

    for n in data:
        if numbers[n]:
            return n * numbers[n]
        else:
            key = 2020 - n
            numbers[key] = n


def triple_sum(data: typing.List[int]):
    data_len = len(data)

    for i in range(data_len - 3):
        for j in range(i + 1, data_len - 2):
            for k in range(j + 1, data_len - 1):
                a, b, c = data[i], data[j], data[k]

                if (a + b + c) == 2020:
                    print(f'Triple numbers answer: {(a, b, c)}')
                    return a * b * c


def main(input_data_path: str):
    data = read_input(input_data_path)
    parsed = parse_data(data)

    print(f'Double sum answer: {double_sum(parsed)}')

    print(f'Three sum answer: {triple_sum(parsed)}')
    
    
