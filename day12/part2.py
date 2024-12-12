from collections import defaultdict
from functools import lru_cache
from itertools import groupby
from typing import List, Set, Tuple

def neighbors(position: Tuple[int, int], map: List[List[str]]) -> List[Tuple[int, int]]: 
    N, M = len(map), len(map[0])
    i, j = position
    neighbors = [(x, y) for x, y in [
        (i-1, j),
        (i, j+1),
        (i+1, j),
        (i, j-1),
    ] if 0 <= x < N and 0 <= y < M and map[x][y] == (map[i][j])]
    return neighbors


def region(position: Tuple[int, int], map: List[List[str]], visited: Set[Tuple[int, int]]):
    sides = defaultdict(list)
    reg = []
    stack = [position]
    N, M = len(map), len(map[0])
    while len(stack) > 0:
        cur = stack.pop()
        if cur not in visited:
            ns = neighbors(cur, map)
            i, j = cur
            if i == 0 or (i-1, j) not in ns:
                sides["UP"].append((i,j))
            if i == N or (i+1, j) not in ns:
                sides["DOWN"].append((i,j))
            if j == 0 or (i, j-1) not in ns:
                sides["LEFT"].append((i,j))
            if j == M or (i, j+1) not in ns:
                sides["RIGHT"].append((i,j))
            fence = 4 - len(ns)
            reg.append((cur, fence))
            stack.extend(ns)
        visited.add(cur)
    return reg, sides


def group_by(l, key):
    collector = defaultdict(list)
    for item in l:
        collector[key(item)].append(item)
    return collector.items()

def count_sides(border, orientation):
    match orientation:
        case "UP":
            group_key, sort_key = lambda x: x[0], lambda x: x[1]
        case "DOWN":
            group_key, sort_key = lambda x: x[0], lambda x: x[1]
        case "LEFT":
            group_key, sort_key = lambda x: x[1], lambda x: x[0]
        case "RIGHT":
            group_key, sort_key = lambda x: x[1], lambda x: x[0]
        case _:
            group_key, sort_key = lambda x: 0, lambda x: 0

    sides = 0
    for _, plots in group_by(border, group_key):
        plots = sorted(plots, key=sort_key)
        prev = None
        for p in plots:
            if prev is None  or prev != sort_key(p)-1:
                sides += 1
            prev = sort_key(p)
    return sides

def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output2.txt"
    else:
        input_path = "input.txt"
        output_path = "output2.txt"
    with open(input_path, "r") as f_in:
        map = [[c for c in line.strip()] for line in f_in.readlines() if line.strip()]
        N, M = len(map), len(map[0])
        visited = set()
        result = 0
        for i in range(N):
            for j in range(M):
                reg, borders = region((i,j), map, visited)
                if reg:
                    sides = 0
                    for orientation, border in borders.items():
                        sides += count_sides(border, orientation)
                    area = len(reg)
                    result += area*sides
                    print(f"- A region of {map[i][j]} plants with price {area} * {sides} = {area*sides}")
    with open(output_path, "w") as f_out:
        f_out.write(str(result))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)