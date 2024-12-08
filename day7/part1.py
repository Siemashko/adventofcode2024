
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
        output_path = "test_output1.txt"
    else:
        input_path = "input.txt"
        output_path = "output1.txt"
    with open(input_path, "r") as f_in:
        lines = f_in.readlines()
        result = 0
        for line in lines:
            test_value_raw, values_raw = line.split(':')
            test_value = int(test_value_raw)
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