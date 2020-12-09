import typing
from copy import deepcopy
from functools import reduce
from operator import mul
from pprint import pprint

from .data_tools import load_array


def parse_data(raw: str) -> typing.List[typing.List[str]]:
    return [list(l) for l in raw.splitlines()]


def count_trees(tree_map: typing.List[typing.List[str]], right: int, down: int) -> int:
    # map_copy = deepcopy(tree_map)
    width = len(tree_map[0])
    x, y = 0, 0
    tree_count = 0
    # print(f'Width of tree map: {width}')
    for i in range(int(len(tree_map) / down)):
        x, y = (right * i) % width, down * i
        print(f'(x, y) = {(x, y)}')
        # map_copy[y][x] = 'X'
        tree_count += 1 if tree_map[y][x] == '#' else 0
    
    return tree_count

    

def main(input_data_path: str):
    parsed = load_array(input_data_path)
    angles = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
    num_trees = [count_trees(parsed, r, d) for r, d in angles]
    product = reduce(mul, num_trees)

    print(f'Number of trees encountered: {product}')
