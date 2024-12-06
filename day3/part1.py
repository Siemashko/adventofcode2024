import re

def mul(x, y):
    return x*y

def main():
    safe_count = 0
    with open("input.txt", "r") as f_in:
        input = f_in.read()
        matches = re.findall(r"mul\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\)", input)
        result = sum(eval(x) for x in matches)

    with open("output1.txt", "w") as f_out:
        f_out.write(str(result))
    print("Done")

if __name__ == "__main__":
    main()