import json
from typing import Dict, Any

class ConnectionInfo:
    def __init__(self, node: str, input: str):
        self.node = node
        self.input = input

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConnectionInfo):
            return False
        return self.node == other.node and self.input == other.input

    def __repr__(self) -> str:
        return f"ConnectionInfo(node={self.node}, input={self.input})"

    def __str__(self) -> str:
        """Return a JSON-like string representation of the object."""
        return json.dumps(self, default=vars)

    def to_dict(self) -> Dict[str, Any]:
        return {"node": self.node, "input": self.input}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConnectionInfo':
        return cls(node=data["node"], input=data["input"])

    def copy(self) -> 'ConnectionInfo':
        return ConnectionInfo(node=self.node, input=self.input)
