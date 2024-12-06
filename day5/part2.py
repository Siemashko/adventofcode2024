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
        lines = f_in.readlines()
        first_section = [tuple(line.strip().split("|")) for line in lines if "|" in line]
        second_section = [line.strip().split(",") for line in lines if "|" not in line and line.strip()]
        forbidden_pages = defaultdict(set)
        for before, after in first_section:
            forbidden_pages[before].add(after)
        result = 0
        incorrectly_ordered = []
        for order in second_section:
            is_valid = True
            pages_checked = set()
            for page in order:
                if len(pages_checked.intersection(forbidden_pages[page])) > 0:
                    is_valid = False
                pages_checked.add(page)
            if not is_valid:
                incorrectly_ordered.append(order)
        for order in incorrectly_ordered:
            filtered_forbidden_pages = {
                key: set(order).intersection(forbidden) for key, forbidden in forbidden_pages.items() if key in set(order)
            }
            new_order = []
            for i in range(len(order)):
                new_forbidden_pages = {}
                for key, forbidden in filtered_forbidden_pages.items():
                    filtered_forbidden_pages
                    if len(forbidden) == 0:
                        new_order.append(key)
                        filtered_forbidden_pages.pop(key)
                        for key2, forbidden2 in filtered_forbidden_pages.items():
                            if not key2 == key:
                                if key in forbidden2: forbidden2.remove(key)
                                new_forbidden_pages[key2] = forbidden2
                        break
                filtered_forbidden_pages = new_forbidden_pages
            new_order = new_order[::-1]
            result += int(new_order[len(order)//2])
        
    with open(output_path, "w") as f_out:
        f_out.write(str(result))
    print("Done")

if __name__ == "__main__":
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print("time elapsed [s]", end - start)