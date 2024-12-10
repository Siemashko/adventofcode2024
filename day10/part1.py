from collections import defaultdict
import curses
import time
from typing import List, Set, Tuple


def neighbors(position: Tuple[int, int], map: List[List[int]]) -> List[Tuple[int, int]]:
    N, M = len(map), len(map[0])
    i, j = position
    neighbors = [(x, y) for x, y in [
        (i-1, j),
        (i, j+1),
        (i+1, j),
        (i, j-1),
    ] if 0 <= x < N and 0 <= y < M and map[x][y] == (map[i][j] + 1)]
    return neighbors


def search(position: Tuple[int, int], map:  List[List[int]], visited: Set[Tuple[int, int]], stdscr: curses.window) -> Tuple[int, Set[Tuple[int, int]]]:
    time.sleep(0.01)
    i, j = position
    stdscr.addstr(i, j, str(map[i][j]))
    stdscr.refresh()
    visited.add(position)
    if map[i][j] == 9:
        return 1
    next_positions = [p for p in neighbors(position, map) if p not in visited]
    peaks = sum(search(p, map, visited, stdscr) for p in next_positions)
    return peaks


def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output1.txt"
    else:
        input_path = "input.txt"
        output_path = "output1.txt"
    with open(input_path, "r") as f_in:
        result = 0
        map = [[int(c) for c in line.strip()] for line in f_in.readlines() if line.strip()]
        N, M = len(map), len(map[0])
        stdscr = curses.initscr()
        curses.noecho()
        results = []
        for i in range(N):
            for j in range(M):
                stdscr.addstr(0, 0, "\n".join(["".join(['.']*M)]*N))
                stdscr.refresh()
                if map[i][j] == 0:
                    peaks = search((i,j), map, set(), stdscr)
                    result += peaks
                    results.append(((i, j), peaks))
                # for k, r in enumerate(results):
                    # stdscr.addstr(N+k, 0, f"{r[0]}: {r[1]}")
                    # stdscr.refresh()
        curses.echo()
        curses.endwin()
        print(results)
    with open(output_path, "w") as f_out:
        f_out.write(str(result))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)