from enum import Enum

class Ports:
    def __init__(self):
        self.ports = [5001,5002]

    def get(self):
        return self.ports

class NodeState(Enum):
    REMOVED = "1"
    FAILED = "2"
    COMMITTED = "3"
    ABORTED = "4"
    INITIAL = "5"
    