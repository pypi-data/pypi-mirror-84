__version__ = "0.1.0"

from . import input, output, matcher
import sys


def run():
    if len(sys.argv) < 2:
        print("Usage: peerfeedback filename.xlsx")
        return 1

    filename = sys.argv[1]
    students = input.read_candidates_from_file(filename=filename)
    mapping = matcher.create_map(students)
    excel_rows = [
        output.generate_row(stud, mapping) for stud in mapping.mappings.keys()
    ]

    out_filename = output.create_output_filename(filename)
    output.write_to_file(rows=excel_rows, filename=out_filename)
    print(f"All done! The output was written to: {out_filename}")
    return 0
