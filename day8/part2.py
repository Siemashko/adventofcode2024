
from collections import defaultdict


def is_divisible(a,b):
    return a % b == 0

def check_operations(test_value, values):
    if len(values) == 0:
        return False
    if len(values) == 1:
        return test_value == values[0]
    valid=False
    if is_divisible(test_value, values[-1]):
        valid = check_operations(test_value/values[-1], values[:-1])
    if valid:
        return valid
    return check_operations(test_value-values[-1], values[:-1])

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
        result = 0
        satellites = defaultdict(list)
        n = len(lines)
        for i, line in enumerate(lines):
            m = len(line.strip())
            for j, x in enumerate(line.strip()):
                if not x == '.':
                    satellites[x].append((i,j))
        unique_anps = set()
        for freq, positions in satellites.items():
            ordered_pairs = []
            for p1 in positions:
                ordered_pairs.extend([(p1, p2) for p2 in positions if not p1 == p2])
            for (p1, p2) in ordered_pairs:
                # translation vector
                tv = p2[0]-p1[0], p2[1]-p1[1]

                # antinode position
                anp = p1[0] + tv[0], p1[1] + tv[1]
                # check if in-bounds
                while 0 <= anp[0] < n and 0 <= anp[1] < m:
                    unique_anps.add(anp)
                    anp = anp[0] + tv[0], anp[1] + tv[1]
        
    with open(output_path, "w") as f_out:
        f_out.write(str(len(unique_anps)))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)