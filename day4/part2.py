import re
import numpy as np
from collections import defaultdict

def main():
    test = False
    if test:
        input_path = "test2.txt"
        output_path = "test_output2.txt"
    else:
        input_path = "input.txt"
        output_path = "output2.txt"
    with open(input_path, "r") as f_in:
        matrix = []
        for line in f_in.readlines():
            matrix.append(list(line.strip()))
        X = np.matrix(matrix)
        n, m = X.shape
        total_count = 0
        for i in range(n-2):
            for j in range(m-2):
                sub_X = X[i:i+3,j:j+3]
                if sub_X[1,1] == "A":
                    counts = defaultdict(lambda: 0)
                    corners = (
                        sub_X[0,0], sub_X[0,2],
                        sub_X[2,0], sub_X[2,2]
                    )
                    allowed_corners = {
                        ("S", "M",
                         "S", "M"),
                        ("M", "S",
                         "M", "S"),
                        ("S", "S",
                         "M", "M"),
                        ("M", "M",
                         "S", "S"),
                    }
                    if corners in allowed_corners:
                        total_count += 1

 
    with open(output_path, "w") as f_out:
        f_out.write(str(total_count))
    print("Done")

if __name__ == "__main__":
    main()