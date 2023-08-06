#!/usr/bin/python3

from dataclasses import dataclass
import typing

@dataclass(frozen=True)
class Candidate:
    email: str

@dataclass
class CandidateMap:
    mappings: typing.Dict[
        Candidate, typing.Tuple[Candidate, Candidate]
    ]
