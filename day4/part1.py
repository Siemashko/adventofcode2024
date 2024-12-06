import re

def main():
    test = False
    if test:
        input_path = "test2.txt"
        output_path = "test_output1.txt"
    else:
        input_path = "input.txt"
        output_path = "output1.txt"
    with open(input_path, "r") as f_in:
        matrix = []
        for line in f_in.readlines():
            matrix.append(line.strip())
        # 8 directions
        count = 0
        # N = number of rows, M = number of cols
        N, M = len(matrix), len(matrix[0])
        # left to right
        for row in matrix:
            count += len(re.findall(r"XMAS", row))
        # right to left
        for row in matrix:
            count += len(re.findall(r"XMAS", row[::-1]))
        # top to bottom
        matrix_transposed = ["".join(row[i] for row in matrix) for i in range(len(matrix[0]))]
        for row in matrix_transposed:
            count += len(re.findall(r"XMAS", row))
        # bottom to top
        for row in matrix_transposed:
            count += len(re.findall(r"XMAS", row[::-1]))

        matrix_rotate_right = []
        # (0, 0)
        # (1, 0), (0, 1)
        # (2, 0), (1, 1), (0, 2)
        # (3, 0), (2, 1), (1, 2), (0, 3)
        # (4, 0), (3, 1), (2, 2), (1, 3), (0, 4)
        # (5, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 5)
        # (6, 0), (5, 1), (4, 2), (3, 3), (2, 4), (1, 5), (0, 6)
        for i in range(N+M-1):
            s = ""
            for j in range(i+1):
                if i-j < N and j < M:
                    print((i-j, j), end=" ")
                    s += matrix[i-j][j]
            print()
            matrix_rotate_right.append(s)

        matrix_rotate_left = []
        # (0, 2)
        # (0, 1), (1, 2)
        # (0, 0), (1, 1), (2, 2)
        # (0, -1), (1, 0), (2, 1), (3, 2)
        # (0, -2), (1, -1), (2, 0), (3, 1), (4, 2)
        for i in range(N+M-1):
            s = ""
            for j in range(i+1):
                k = M - i - 1
                if j < N and 0 <= k + j:
                    print((j, k+j), end=" ")
                    s += matrix[j][k+j]
            print()
            matrix_rotate_left.append(s)
        # top left to bottom right
        for row in matrix_rotate_left:
            count += len(re.findall(r"XMAS", row))
        # bottom right to top left
        for row in matrix_rotate_left:
            count += len(re.findall(r"XMAS", row[::-1]))
        # bottom left to top right
        for row in matrix_rotate_right:
            count += len(re.findall(r"XMAS", row))
        # top right to bottom left
        for row in matrix_rotate_right:
            count += len(re.findall(r"XMAS", row[::-1]))
        for row in matrix:
            print(row)
        print()
        for row in matrix_transposed:
            print(row)
        print()
        for row in matrix_rotate_left:
            print(row)
        print()
        for row in matrix_rotate_right:
            print(row)
        print()

 
    with open(output_path, "w") as f_out:
        f_out.write(str(count))
    print("Done")

if __name__ == "__main__":
    main()