#!/usr/bin/python3

import re
import typing
import pandas

from peerfeedback.interfaces import Candidate

def read_candidates_from_file(filename: str) -> typing.List["Candidate"]:
    """Read Candidates for a CSV Sheet"""
    candidate_list = []
    with open(filename, mode="rb") as excelfile:
        df = pandas.read_excel(excelfile)
        input_dict = df.to_dict()
        for row in input_dict.values():
            for col in row.values():
                candidate = parse_candidate(col)
                if candidate:
                    candidate_list.append(candidate)

    return candidate_list


def parse_candidate(string: str) -> typing.Union["Candidate", None]:
    """Parse Candidate from given string."""
    regex = re.compile(r"^\w+\.\w+@stud\.leuphana\.de$")
    if regex.match(string.strip()):
        return Candidate(string)
    else:
        return None

