import json
from typing import List, Dict, Any

from OutputInfo import OutputInfo

class NodeInfo:
    def __init__(self, name: str, data: Dict[str, Any], custom_class: str, component: str, inputs: List[str], outputs: Dict[str, OutputInfo], pos_x: float, pos_y: float):
        self.name = name
        self.data = data
        self.custom_class = custom_class
        self.component = component
        self.inputs = inputs
        self.outputs = outputs
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NodeInfo):
            return False
        return (
            self.name == other.name and
            self.data == other.data and
            self.custom_class == other.custom_class and
            self.component == other.component and
            self.inputs == other.inputs and
            self.outputs == other.outputs and
            self.pos_x == other.pos_x and
            self.pos_y == other.pos_y
        )

    def __repr__(self) -> str:
        return f"NodeInfo(name={self.name}, data={self.data}, custom_class={self.custom_class}, component={self.component}, inputs={self.inputs}, outputs={self.outputs}, pos_x={self.pos_x}, pos_y={self.pos_y})"

    def __str__(self) -> str:
        """Return a JSON-like string representation of the object."""
        return json.dumps(self, default=vars)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "data": self.data,
            "class": self.custom_class,
            "component": self.component,
            "inputs": self.inputs,
            "outputs": {k: v.to_dict() for k, v in self.outputs.items()},
            "pos_x": self.pos_x,
            "pos_y": self.pos_y
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NodeInfo':
        outputs = {k: OutputInfo.from_dict(v) for k, v in data.get("outputs", {}).items()}
        return cls(
            name=data["name"],
            data=data["data"],
            custom_class=data["class"],
            component=data["component"],
            inputs=data["inputs"],
            outputs=outputs,
            pos_x=data["pos_x"],
            pos_y=data["pos_y"]
        )

    def copy(self) -> 'NodeInfo':
        return NodeInfo(
            name=self.name,
            data=self.data.copy(),
            custom_class=self.custom_class,
            component=self.component,
            inputs=self.inputs.copy(),
            outputs={k: v.copy() for k, v in self.outputs.items()},
            pos_x=self.pos_x,
            pos_y=self.pos_y
        )
