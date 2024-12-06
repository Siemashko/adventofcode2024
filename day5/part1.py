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
        lines = f_in.readlines()
        first_section = [tuple(line.strip().split("|")) for line in lines if "|" in line]
        second_section = [line.strip().split(",") for line in lines if "|" not in line and line.strip()]
        forbidden_pages = defaultdict(set)
        for before, after in first_section:
            forbidden_pages[before].add(after)
        result = 0
        for order in second_section:
            is_valid = True
            pages_checked = set()
            for page in order:
                if len(pages_checked.intersection(forbidden_pages[page])) > 0:
                    is_valid = False
                pages_checked.add(page)
            if is_valid:
               result += int(order[len(order)//2])
        
    with open(output_path, "w") as f_out:
        f_out.write(str(result))
    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)