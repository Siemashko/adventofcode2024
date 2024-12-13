import re

A_COST = 3
B_COST = 1

def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output1.txt"
    else:
        input_path = "input.txt"
        output_path = "output1.txt"
    result = 0
    with open(input_path, "r") as f_in:
        lines = f_in.readlines()
        with open('log.txt', "a") as log_f:
            for i in range(0,len(lines), 4):
                a = int(re.search(r'X\+([0-9]+)', lines[i]).group(1)), int(re.search(r'Y\+([0-9]+)', lines[i]).group(1))
                b = int(re.search(r'X\+([0-9]+)', lines[i+1]).group(1)), int(re.search(r'Y\+([0-9]+)', lines[i+1]).group(1))
                prize = int(re.search(r'X=([0-9]+)', lines[i+2]).group(1)), int(re.search(r'Y=([0-9]+)', lines[i+2]).group(1))
                a0, a1 = a
                b0, b1 = b
                c0, c1 = prize
                # X * A0 + Y * B0 = C0
                # X * A1 + Y * B1 = C1
                # ------------
                # Y = (C1 - X*A1)/B1
                # X * A0 + (C1 - X*A1)*B0/B1 = C0
                # X * B1 * A0 + (C1 - X*A1) * B0 = C0 * B1
                # X * (B1 * A0 - A1 * B0) = C0 * B1 - C1 * B0
                # X = (C0 * B1 - C1 * B0) / (B1 * A0 - A1 * B0)
                # Y = (C0 * A1 - C1 * A0) / (B1 * A0 - A1 * B0)
                xc = c0 * b1 - c1 * b0
                if xc % (b1 * a0 - a1 * b0) == 0:
                    x = xc // (b1 * a0 - a1 * b0)
                    yc = c1 - x*a1
                    if yc % b1 == 0:
                        y = yc // b1
                        result += x*A_COST + y*B_COST
    with open(output_path, "w") as f_out:
        f_out.write(str(result))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)