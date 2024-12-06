import re

def main():
    with open("input.txt", "r") as f_in:
        a_s = []
        b_s = []
        while line := f_in.readline():
            a, b = re.split(r"\s+", line.strip())
            a_s.append(int(a))
            b_s.append(int(b))
    result = sum(abs(x-y) for x, y in zip(sorted(a_s), sorted(b_s)))
    with open("output1.txt", "w") as f_out:
        f_out.write(str(result))
    print("Done")

if __name__ == "__main__":
    main()