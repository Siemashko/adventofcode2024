from collections import defaultdict
from functools import lru_cache
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
    reg = []
    stack = [position]
    while len(stack) > 0:
        cur = stack.pop()
        if cur not in visited:
            ns = neighbors(cur, map)
            fence = 4 - len(ns)
            reg.append((cur, fence))
            stack.extend(ns)
        visited.add(cur)
    return reg

def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output1.txt"
    else:
        input_path = "input.txt"
        output_path = "output1.txt"
    with open(input_path, "r") as f_in:
        map = [[c for c in line.strip()] for line in f_in.readlines() if line.strip()]
        N, M = len(map), len(map[0])
        visited = set()
        result = 0
        for i in range(N):
            for j in range(M):
                reg = region((i,j), map, visited)
                if reg:
                    area = len(reg)
                    perimeter = sum(p[1] for p in reg)
                    result += area*perimeter
                    print(f"- A region of {map[i][j]} plants with price {area} *  {perimeter} = {area*perimeter}")
    with open(output_path, "w") as f_out:
        f_out.write(str(result))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)