import csv
import sys

def longest_match(sequence, subsequence):
    longest_run = 0
    sub_len = len(subsequence)
    seq_len = len(sequence)

    for i in range(seq_len):
        count = 0
        while sequence[i + count * sub_len : i + (count + 1) * sub_len] == subsequence:
            count += 1
        longest_run = max(longest_run, count)

    return longest_run

def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        str_names = reader.fieldnames[1:]  # exclude the first column which is 'name'
        people = list(reader)

    with open(sys.argv[2], 'r') as file:
        dna_sequence = file.read()

    str_counts = {str_name: longest_match(dna_sequence, str_name) for str_name in str_names}

    for person in people:
        if all(str_counts[str_name] == int(person[str_name]) for str_name in str_names):
            print(person['name'])
            return

    print("No match")


main()
