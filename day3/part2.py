import re

def mul(x, y):
    return x*y

def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output2.txt"
    else:
        input_path = "input.txt"
        output_path = "output2.txt"
    with open(input_path, "r") as f_in:
        input = f_in.read()
        matches = re.findall(r"mul\([1-9][0-9]{0,2},[1-9][0-9]{0,2}\)|do\(\)|don't\(\)", input)
        result = 0
        print(matches)
        do = True
        for x in matches:
            if x == "do()":
                do = True
                continue
            if x == "don't()":
                do = False
                continue
            if do: result += eval(x)
 
    with open(output_path, "w") as f_out:
        f_out.write(str(result))
    print("Done")

if __name__ == "__main__":
    main()