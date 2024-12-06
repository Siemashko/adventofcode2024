import re

def is_safe(x0, xs, decreasing=False, allow_skip=True) -> bool:
    if len(xs) == 0:
        return True
    if (x0 > xs[0] if decreasing else x0 < xs[0]) and 1 <= abs(x0-xs[0]) <= 3:
        return is_safe(xs[0], xs[1:], decreasing=decreasing)
    return False

def is_safe2(xs):
    diffs = [x-y for x, y in zip(xs, xs[1:])]
    print(diffs)
    ### All in [1,3]
    print("in [1,3]", all(1 <= abs(diff) <= 3 for diff in diffs))
    if not all(1 <= abs(diff) <= 3 for diff in diffs):
        return False
    if all(diff < 0 for diff in diffs) or all(diff > 0 for diff in diffs):
        return True
    return False

def main():
    safe_count = 0
    with open("input.txt", "r") as f_in:
        for line in f_in.readlines():
            xs = [int(x) for x in re.split(r"\s+", line.strip())]
            diffs = [x-y for x, y in zip(xs, xs[1:])]
            if is_safe2(xs):
                safe_count += 1
            else:
                for i in range(len(xs)):
                    new_xs = xs[:i] + xs[i+1:]
                    if is_safe2(new_xs):
                        safe_count += 1
                        break
    with open("output3.txt", "w") as f_out:
        f_out.write(str(safe_count))
    print("Done")

if __name__ == "__main__":
    main()