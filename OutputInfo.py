import json
from typing import List, Dict, Any

from ConnectionInfo import ConnectionInfo

class OutputInfo:
    def __init__(self, connections: List[ConnectionInfo] = None):
        self.connections = connections or []

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OutputInfo):
            return False
        return self.connections == other.connections

    def __repr__(self) -> str:
        return f"Output(connections={self.connections})"

    def __str__(self) -> str:
        """Return a JSON-like string representation of the object."""
        return json.dumps(self, default=vars)

    def to_dict(self) -> Dict[str, Any]:
        return {"connections": [conn.to_dict() for conn in self.connections]}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OutputInfo':
        connections = [ConnectionInfo.from_dict(conn) for conn in data.get("connections", [])]
        return cls(connections=connections)

    def copy(self) -> 'OutputInfo':
        return OutputInfo(connections=[conn.copy() for conn in self.connections])