import re

def is_safe(x0, xs, decreasing=False) -> bool:
    if len(xs) == 0:
        return True
    if (x0 > xs[0] if decreasing else x0 < xs[0]) and 1 <= abs(x0-xs[0]) <= 3:
        return is_safe(xs[0], xs[1:], decreasing=decreasing)
    return False

def main():
    safe_count = 0
    with open("input.txt", "r") as f_in:
        for line in f_in.readlines():
            xs = [int(x) for x in re.split(r"\s+", line.strip())]
            safe_count += is_safe(xs[0], xs[1:], decreasing=xs[0]>xs[1])

    with open("output1.txt", "w") as f_out:
        f_out.write(str(safe_count))
    print("Done")

if __name__ == "__main__":
    main()