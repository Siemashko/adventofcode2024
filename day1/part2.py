from collections import defaultdict
import re
def main():
    with open("input.txt", "r") as f_in:
        a_s = []
        b_s = []
        while line := f_in.readline():
            a, b = re.split(r"\s+", line.strip())
            a_s.append(int(a))
            b_s.append(int(b))
    b_counts = defaultdict(lambda: 0)
    for b in b_s:
        b_counts[b] += 1
    result = sum(a*b_counts[a] for a in a_s)
    with open("output2.txt", "w") as f_out:
        f_out.write(str(result))
    print("Done")

if __name__ == "__main__":
    main()