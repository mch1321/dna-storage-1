import copy as cp
from dataclasses import dataclass


class Path:
    def __init__(self, init_state):
        self.tip = init_state
        self.length = 0
        self.visited = [init_state]
        self.distances = [0]
        self.observations = ""
        self.sequence = ""

    def extend(self, new_state, distance, input, output):
        self.tip = new_state
        self.length += distance
        self.visited.append(new_state)
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
