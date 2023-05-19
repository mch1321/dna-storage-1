import copy as cp
from dataclasses import dataclass


class Path:
    def __init__(self, initState):
        self.tip = initState
        self.length = 0
        self.visited = [initState]
        self.distances = [0]
        self.observations = ""
        self.sequence = ""

    def extend(self, newState, distance, input, output):
        self.tip = newState
        self.length += distance
        self.visited.append(newState)
        self.distances.append(distance)
        self.sequence += input
        self.observations += output

    def copy(self):
        return cp.deepcopy(self)


@dataclass
class Transition:
    start: str
    next: str
    input: str
    output: str

    def __str__(self):
        return f"{self.start} + {self.input}/{self.output} -> {self.next}"
