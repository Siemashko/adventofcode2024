from collections import defaultdict
from typing import Tuple, Set
import numpy as np
import enum
import curses, time

class GuardDirection(enum.Enum):
    UP = "^"
    DOWN = "v"
    RIGHT = ">"
    LEFT = "<"

def add(x1, x2):
    x1_0, x1_1 = x1
    x2_0, x2_1 = x2
    return (x1_0+x2_0, x1_1+x2_1)

def to_tuple(array):
    return int(array[0]), int(array[1])

class MapGaurd():

    map: np.matrix
    guard_position: Tuple[int, int]
    guard_direction: GuardDirection
    obstacles: Set[Tuple[int, int]]
    visited: Set[Tuple[int, int]]
    display_width: int
    display_height: int

    def __init__(self, map, display_width=40, display_height=40):
        self.map = map
        self.display_width = display_width
        self.display_height = display_height
        self.guard_position = to_tuple(np.argwhere(
            np.logical_or.reduce([
                map == GuardDirection.UP.value,
                map == GuardDirection.DOWN.value,
                map == GuardDirection.RIGHT.value,
                map == GuardDirection.LEFT.value,
            ])
        )[0])
        self.guard_direction = GuardDirection._value2member_map_[self.map[self.guard_position]]
        self.obstacles = set([to_tuple(obstacle) for obstacle in np.argwhere(self.map == "#")])
        self.visited = set()

    def get_increment(self):
        match self.guard_direction:
            case GuardDirection.UP:
                return (-1, 0)
            case GuardDirection.RIGHT:
                return (0, 1)
            case GuardDirection.DOWN:
                return (1, 0)
            case GuardDirection.LEFT:
                return (0, -1)
            case _:
                return (0, 0)
    
    def rotate_right(self):
        match self.guard_direction:
            case GuardDirection.UP:
                self.guard_direction = GuardDirection.RIGHT
            case GuardDirection.RIGHT:
                self.guard_direction = GuardDirection.DOWN
            case GuardDirection.DOWN:
                self.guard_direction = GuardDirection.LEFT
            case GuardDirection.LEFT:
                self.guard_direction = GuardDirection.UP
            case _:
                pass

    def step(self):
        if self.is_done():
            print("The Guard has left the mapped area")
        next_position = add(self.guard_position, self.get_increment())
        if next_position in self.obstacles:
            self.rotate_right()
        else:
            self.visited.add(self.guard_position)
            self.guard_position = next_position

    def is_done(self):
        N, M = self.map.shape
        i, j = self.guard_position
        return not (0 <= i <= N-1 and 0 <= j <= M-1)
    
    @property
    def result(self):
        return len(self.visited)
    
    def __repr__(self):
        show_trace = True
        N, M = self.map.shape
        repr_map = np.matrix([['.']*M]*N)
        for obstacle in self.obstacles:
            repr_map[obstacle] = "#"
        if show_trace:
            for v in self.visited:
                repr_map[v] = "X"
        if not self.is_done():
            repr_map[self.guard_position] = self.guard_direction.value
        i, j = self.guard_position
        def get_window(p, d, m):
            if p <= d//2:
                window = 0, d
            elif p + d//2 >= m:
                window = m-d-1, m
            else:
                window = p-d//2, p+d//2
            return window

        hr = get_window(i, self.display_height, N)
        vr = get_window(j, self.display_width, M)
        limited_repr_map = repr_map[hr[0]:hr[1],vr[0]:vr[1]]
        return "\n".join([" ".join(line) for line in limited_repr_map.tolist()])


def main():
    test = True
    if test:
        input_path = "test.txt"
        output_path = "test_output1.txt"
    else:
        input_path = "input.txt"
        output_path = "output1.txt"
    with open(input_path, "r") as f_in:
        lines = f_in.readlines()
        map = np.matrix(
            [
                [x for x in line.strip()]
                for line in lines if line.strip()
            ]
        )
        map_guard = MapGaurd(map)
        stdscr = curses.initscr()
        curses.noecho()
        while not map_guard.is_done():
            map_guard.step()
            stdscr.addstr(0, 0, str(map_guard))
            stdscr.refresh()
        curses.echo()
        curses.endwin()
        result = map_guard.result
        
    with open(output_path, "w") as f_out:
        f_out.write(str(result))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)