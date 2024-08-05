import json
from typing import Dict, Any, List

from NodeInfo import NodeInfo

class DrawflowInfo:
    def __init__(self, nodes: Dict[str, NodeInfo]):
        self._nodes = nodes

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DrawflowInfo):
            return False
        return self._nodes == other.nodes

    def __repr__(self) -> str:
        return f"DrawflowInfo(nodes={self._nodes})"

    def __str__(self) -> str:
        """Return a JSON-like string representation of the object."""
        return json.dumps(self, default=vars)

    def to_dict(self) -> Dict[str, Any]:
        return {node_id: node.to_dict() for node_id, node in self._nodes.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DrawflowInfo':
        nodes = {k: NodeInfo.from_dict(v) for k, v in data.items()}
        return cls(nodes=nodes)

    def copy(self) -> 'DrawflowInfo':
        return DrawflowInfo(nodes={k: v.copy() for k, v in self._nodes.items()})
    
    def __getitem__(self, item):
         return self._nodes[item]
     
    def remove(self, node_id: str):
        del self._nodes[node_id]
        
    def list_nodes(self) -> List[str]:
        return list(self._nodes.keys())
    
    def __del__(self):
        self._nodes.clear()
