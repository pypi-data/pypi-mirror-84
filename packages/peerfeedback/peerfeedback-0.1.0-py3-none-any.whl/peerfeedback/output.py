#!/usr/bin/python3

import textwrap
import typing
import os.path
from peerfeedback.interfaces import Candidate, CandidateMap

import pandas


def get_recipients(
    candidate: Candidate, candidates: CandidateMap
) -> typing.Tuple[Candidate, Candidate]:
    """Get the tuple of students the passed student is giving feedback to."""
    return candidates.mappings[candidate]


def get_providers(
    candidate: Candidate, candidates: CandidateMap
) -> typing.Tuple[Candidate, Candidate]:
    """Get the tuple of students that provide feedback to the passed student."""
    ret = tuple(stud for stud, pair in candidates.mappings.items() if candidate in pair)

    if len(ret) != 2:
        raise ValueError("Wrong number of providers.")

    return ret


def generate_email(candidate: Candidate, candidate_map: CandidateMap) -> str:
    recipients = get_recipients(candidate, candidate_map)
    providers = get_providers(candidate, candidate_map)
    return textwrap.dedent(
        """
    Dear students,
    below you will find your peer students.

    You will give feedback to
    {recipient1}
    {recipient2}

    And receive feedback from
    {provider1}
    {provider2}
    """.format(
            recipient1=recipients[0].email,
            recipient2=recipients[1].email,
            provider1=providers[0].email,
            provider2=providers[1].email,
        )
    )


def generate_row(candidate: Candidate, candidate_map: CandidateMap):
    """Generate a row the Excel output. The format is:

        student recipent1 recipient2 provider1 provider2

    With recipients being the persons that "student" gives feedback to and
    providers being the persons that "student" receives feedback from.
    """
    recipients = get_recipients(candidate, candidate_map)
    providers = get_providers(candidate, candidate_map)
    return (
        candidate.email,
        recipients[0].email,
        recipients[1].email,
        providers[0].email,
        providers[1].email,
    )


def write_to_file(rows: typing.List, filename: str) -> None:
    with pandas.ExcelWriter(filename, mode="w", engine="xlsxwriter") as writer:
        df = pandas.DataFrame(
            rows,
            columns=[
                "Candidate",
                "Recipient 1",
                "Recipient 2",
                "Provider 1",
                "Provider 2",
            ],
        )
        df.to_excel(writer, sheet_name="output", index=False)


def create_output_filename(filename: str) -> str:
    orig_name, ext = os.path.splitext(filename)
    return f"{orig_name}_output{ext}"
