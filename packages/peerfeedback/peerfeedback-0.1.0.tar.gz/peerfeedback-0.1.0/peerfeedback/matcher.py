#!/usr/bin/python3

import typing
from peerfeedback.interfaces import Candidate, CandidateMap


def create_map(candidates: typing.List[Candidate]) -> CandidateMap:
    """
    Create Mapping between students according to the following algorithm.

    n..n(max-2): n: n+1, n+2
    n(max-1): n(max), n(0)
    n(max): n(0), n(1)

    """
    candidate_map = CandidateMap({})
    for i, candidate in enumerate(candidates[:-2]):
       candidate_map.mappings[candidate] = (candidates[i+1], candidates[i+2])

    candidate_map.mappings[candidates[-2]] = (candidates[-1], candidates[0])
    candidate_map.mappings[candidates[-1]] = (candidates[0], candidates[1])

    return candidate_map
