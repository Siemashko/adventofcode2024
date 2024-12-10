from collections import defaultdict


def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output1.txt"
    else:
        input_path = "input.txt"
        output_path = "output1.txt"
    with open(input_path, "r") as f_in:
        diskmap = [int(c) for c in f_in.read().strip()]
        checksum = 0
        fileblocks = diskmap[::2]
        freeblocks = diskmap[1::2]
        is_free = False
        cur_l, cur_r = 0, len(fileblocks)-1
        cur_free = 0
        for i in range(sum(fileblocks)):
            if not is_free and fileblocks[cur_l] == 0:
                is_free = True
                cur_l += 1
            if is_free and freeblocks[cur_free] == 0:
                is_free = False
                cur_free += 1
            if is_free:
                if fileblocks[cur_r] == 0:
                    cur_r -= 1
                checksum += i*cur_r
                fileblocks[cur_r] -= 1
                freeblocks[cur_free] -= 1
            else:
                checksum += i*cur_l
                fileblocks[cur_l] -= 1
        
    with open(output_path, "w") as f_out:
        f_out.write(str(checksum))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)