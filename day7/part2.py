
from typing import List, Optional


def is_divisible(a,b):
    return a % b == 0

def is_prefix_matching(a, prefix):
    if len(str(a)) >= len(str(prefix)):
        return str(a)[:len(str(prefix))] == str(prefix)
    return False

def is_suffix_matching(a, suffix):
    if len(str(a)) >= len(str(suffix)):
        return str(a)[-len(str(suffix)):] == str(suffix)
    return False



def check_operations(test: int, xs: List[int]):
    if test < 0:
        return False
    if len(xs) == 0:
        return False
    if len(xs) == 1:
        return test == xs[0]
    
    x = xs[-1]
    new_xs = xs[:-1]
    valid = False
    try:
        if is_suffix_matching(test, x):
            if not (test == x and len(new_xs) > 0):
                valid = check_operations(int(str(test)[:-len(str(x))]), new_xs)
    except Exception as e:
        raise e
    if not valid and is_divisible(test, x):
        valid = check_operations(int(test/x), new_xs)
    
    return valid or check_operations(int(test-x), new_xs)


def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output3.txt"
    else:
        input_path = "input.txt"
        output_path = "output2.txt"
    with open(input_path, "r") as f_in:
        lines = f_in.readlines()
        result = 0
        for i, line in enumerate(lines):
            test_value_raw, values_raw = line.split(':')
            test_value = int(test_value_raw)
            # Values are provided in reverse order
            values = [int(val) for val in values_raw.strip().split(' ')]
            if check_operations(test_value, values):
                result += test_value
        
    with open(output_path, "w") as f_out:
        f_out.write(str(result))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)