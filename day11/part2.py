from collections import defaultdict
import curses
import time
from typing import List, Set, Tuple

def step(stone: int) -> List[int]:
    if stone == 0:
        return [1]
    if len(str(stone)) % 2 == 0:
        p = len(str(stone)) // 2
        l, r = int(str(stone)[:p]), int(str(stone)[p:])
        return [l, r]
    return [stone*2024]

cache = {}

def get_count(stone: int, blinks: int):
    if blinks <= 0:
        return 1
    if (stone, blinks) in cache:
        return cache[(stone, blinks)]
    count = None
    if stone == 0:
        count = get_count(1, blinks-1)
    elif len(str(stone)) % 2 == 0:
        p = len(str(stone)) // 2
        l, r = int(str(stone)[:p]), int(str(stone)[p:])
        count = get_count(l, blinks-1) + get_count(r, blinks-1)
    else:
        count = get_count(2024*stone, blinks-1)
    cache[(stone, blinks)] = count
    return count

def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output2.txt"
    else:
        input_path = "input.txt"
        output_path = "output2.txt"
    with open(input_path, "r") as f_in:
        result = 0
        stones = [int(n) for n in f_in.read().strip().split(' ')]
        blinks = 75
        result = sum(get_count(s, blinks) for s in stones)
    with open(output_path, "w") as f_out:
        f_out.write(str(result))


    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)