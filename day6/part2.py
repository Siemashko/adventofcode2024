from collections import defaultdict
import copy
from typing import Tuple, Set, Dict, Optional
import numpy as np
import enum
import curses, time
from timeit import default_timer as timer

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

class MapGuard():

    stdscr: curses.window
    map: np.matrix
    guard_position: Tuple[int, int]
    guard_direction: GuardDirection
    obstacles: Set[Tuple[int, int]]
    indexed_obstacles: Dict[int, Dict[int, Optional[Tuple[int, int]]]]
    visited: Dict[Tuple[int, int], Set[GuardDirection]]
    visited_bigraph: Dict[int, Set[int]]
    display_width: int
    display_height: int

    def __init__(self, map, stdscr, display_width=40, display_height=40):
        self.map = map
        self.stdscr = stdscr
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
        self.starting_position = self.guard_position
        self.guard_direction = GuardDirection._value2member_map_[self.map[self.guard_position]]
        self.obstacles = set([to_tuple(obstacle) for obstacle in np.argwhere(self.map == "#")])
        self.visited = defaultdict(lambda: set())
        self.loop_obstacles = set()
        self.visited_bigraph = defaultdict(lambda: set())

    def get_increment_for_direction(self, guard_direction):
        match guard_direction:
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

    def get_increment(self):
        return self.get_increment_for_direction(self.guard_direction)
    
    def get_rotate_right_direction(self, guard_direction):
        match guard_direction:
            case GuardDirection.UP:
                return GuardDirection.RIGHT
            case GuardDirection.RIGHT:
                return GuardDirection.DOWN
            case GuardDirection.DOWN:
                return GuardDirection.LEFT
            case GuardDirection.LEFT:
                return GuardDirection.UP
            case _:
                pass

    def rotate_right(self):
        self.guard_direction = self.get_rotate_right_direction(self.guard_direction)

    def check_loop_obstacle(self, position):
        new_obstacle = add(position, self.get_increment())
        new_obstacles = self.obstacles.union({new_obstacle})
        new_visited = copy.deepcopy(self.visited)
        N, M = self.map.shape
        if not (0 <= new_obstacle[0] < N and 0 <= new_obstacle[1] < M):
            return False
        new_direction = self.get_rotate_right_direction(self.guard_direction)
        current = position
        while 0 <= current[0] < N and 0 <= current[1] < M:
            if new_direction in new_visited[current]:
                return True
            else:
                increment = self.get_increment_for_direction(new_direction)
                new_position = add(current, increment)
                if new_position in new_obstacles:
                    new_direction = self.get_rotate_right_direction(new_direction)
                else:
                    new_visited[current].add(new_direction)
                    current = new_position
        return False

    def step(self):
        next_position = add(self.guard_position, self.get_increment())
        self.stdscr.addstr(6, 0, str(self.guard_position))
        self.stdscr.addstr(7, 0, str(self.is_done()))
        self.stdscr.addstr(8, 0, str(self.is_loop()))
        if self.is_done() or self.is_loop():
            return
        self.visited[self.guard_position].add(self.guard_direction)  
        if next_position in self.obstacles:
            self.rotate_right()
        else:
            self.guard_position = next_position

    def is_done(self):
        N, M = self.map.shape
        i, j = self.guard_position
        return not (0 <= i <= N-1 and 0 <= j <= M-1)
    
    def is_loop(self):
        next_position = add(self.guard_position, self.get_increment())
        return self.guard_direction in self.visited[next_position]

    @property
    def result(self):
        return len(self.visited)
    
    def repr_helper(self, obstacles, loop_obstacles, visited, guard_position, guard_direction, show_trace=True):
        N, M = self.map.shape
        repr_map = np.matrix([['.']*M]*N)
        for obstacle in obstacles:
            repr_map[obstacle] = "#"
        if show_trace:
            for v, directions in visited.items():
                if len(directions) > 0:
                    repr_map[v] = "X"
        if not self.is_done():
            repr_map[guard_position] = guard_direction.value
        i, j = guard_position
        for obstacle in loop_obstacles:
            repr_map[obstacle] = "O"
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

    def __repr__(self):
        return self.repr_helper(
            self.obstacles,
            self.loop_obstacles,
            self.visited,
            self.guard_position,
            self.guard_direction,
        )

    @property
    def loop_obstacles_str(self):
        N, M = self.map.shape
        repr_map = np.matrix([['.']*M]*N)
        for obstacle in self.obstacles:
            repr_map[obstacle] = "#"
        for obstacle in self.loop_obstacles:
            repr_map[obstacle] = "O"
        return "\n".join([" ".join(line) for line in repr_map.tolist()])

def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output2.txt"
    else:
        input_path = "input.txt"
        output_path = "output2.txt"
    with open(input_path, "r") as f_in:
        lines = f_in.readlines()
        map = np.matrix(
            [
                [x for x in line.strip()]
                for line in lines if line.strip()
            ]
        )
        stdscr = curses.initscr()
        curses.noecho()
        start = timer()
        loop_obstacles = set()
        map_guard = MapGuard(map, stdscr)
        while not map_guard.is_done():
            map_guard.step()
            end = timer()
        stdscr.addstr(0, 0, f"time elapsed [s] {end - start}")
        stdscr.addstr(1, 0, "First run done")
        stdscr.addstr(2, 0, str(map_guard))
        stdscr.refresh()
        stdscr.clear()
        visited = set([position for position, directions in map_guard.visited.items() if len(directions) > 0])
        count = 0
        N, M = map.shape
        for i, (v_i, v_j) in enumerate(visited):
                end = timer()
                stdscr.addstr(0, 0, f"time elapsed [s] {end - start}")
                stdscr.addstr(1, 0, f"{i}/{len(visited)}")
                stdscr.refresh()
                if map[v_i, v_j] == ".":
                    new_map = copy.deepcopy(map)
                    new_map[v_i, v_j] = "#"
                    map_guard = MapGuard(new_map, stdscr)
                    step_counter = 0
                    while not map_guard.is_done() and not map_guard.is_loop():
                        if (v_i, v_j) == (36, 37):
                            time.sleep(0.05)
                            stdscr.addstr(10, 0, str(map_guard))
                            stdscr.refresh()
                        map_guard.step()
                        stdscr.addstr(3, 0, f"Steps: {step_counter}")
                        step_counter += 1
                    if map_guard.is_loop():
                        loop_obstacles.add((v_i, v_j))
        curses.echo()
        curses.endwin()
        
    with open(output_path, "w") as f_out:
        f_out.write(str(len(loop_obstacles)))

    print("Done")

if __name__ == "__main__":
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)