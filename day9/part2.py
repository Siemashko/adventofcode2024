from collections import defaultdict


def main():
    test = False
    if test:
        input_path = "test.txt"
        output_path = "test_output2.txt"
    else:
        input_path = "input.txt"
        output_path = "output2.txt"
    with open(input_path, "r") as f_in:
        diskmap = [int(c) for c in f_in.read().strip()]
        checksum = 0
        fileblocks = diskmap[::2]
        checked = [False]*len(fileblocks)
        ix = 0
        for i, block in enumerate(diskmap):
            if i % 2 == 0:
                if not checked[i//2]:
                    for j in range(ix, ix+block):
                        # print(i//2, end='')
                        checksum += (i//2)*j
                    checked[i//2] = True
                # else:
                #     # print(''.join(['.']*block), end='')
            if i % 2 == 1:
                # freespace
                fs = block
                # intermediate index for the free space
                iix = 0
                # find the fileblock with the largest index that fits into the freespace
                while True:
                    blocks = [(j, b) for j, b in enumerate(fileblocks) if not checked[j] and b <= fs]
                    if len(blocks) == 0:
                        break
                    # largest block index
                    lbi, lb = max(blocks, key=lambda x: x[0])
                    # print(lbi, lb)
                    # size of the largest block index
                    for j  in range(ix+iix, ix+iix+lb):
                        # print(lbi, end='')
                        checksum += j*lbi
                    checked[lbi] = True
                    iix += lb
                    fs -= lb
                # if block-iix > 0:
                #     print(''.join(['.']*(block-iix)), end='')
            ix += block
        
    with open(output_path, "w") as f_out:
        f_out.write(str(checksum))

    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)