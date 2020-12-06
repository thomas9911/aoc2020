def prepare(input):
    groups = input.split("\n\n")
    return [x.splitlines() for x in groups]


def do_a(input):
    people = prepare(input)

    groups_sets = [set("".join(x)) for x in people]
    combined_lengths = sum([len(x) for x in groups_sets])
    return combined_lengths


def gather_set(group):
    group_set = None
    for people in group:
        answers = set(people)
        if group_set is None:
            group_set = answers
            continue
        group_set = group_set.intersection(answers)
    return group_set or set()


def count_questions(people_groups):
    count = 0
    for group in people_groups:
        group_set = gather_set(group)
        count += len(group_set)
    return count


def do_b(input):
    people_groups = prepare(input)
    return count_questions(people_groups)


if __name__ == "__main__":
    with open("data.txt") as f:
        # print(do_a(f.read()))
        print(do_b(f.read()))
