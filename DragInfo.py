import json
from typing import Optional, Tuple

from Rectangles import Rectangles
from DrawflowInfo import DrawflowInfo

class DragInfo:
    DECIMAL_POSITIONS = 1
    
    def __init__(
        self,
        *,
        is_dragging: Optional[bool] = None,
        is_dragging_node: bool = False,
        is_dragging_connection: bool = False,
        is_dragging_viewport: bool = False,
        node_id: Optional[str] = None,
        output_name: Optional[str] = None,
        input_name: Optional[str] = None,
        start_x: float = 0,
        start_y: float = 0,
        offset_x: float = 0,
        offset_y: float = 0,
        current_x: float = 0,
        current_y: float = 0,
    ):
        self.is_dragging = is_dragging if is_dragging is not None else (is_dragging_node or is_dragging_connection or is_dragging_viewport)
        self.is_dragging_node = is_dragging_node
        self.is_dragging_connection = is_dragging_connection
        self.is_dragging_viewport = is_dragging_viewport
        self.node_id = node_id
        self.output_name = output_name
        self.input_name = input_name
        self.start_x = DragInfo.rounded_number(start_x)
        self.start_y = DragInfo.rounded_number(start_y)
        self.offset_x = DragInfo.rounded_number(offset_x)
        self.offset_y = DragInfo.rounded_number(offset_y)
        self.current_x = DragInfo.rounded_number(current_x)
        self.current_y = DragInfo.rounded_number(current_y)

    @classmethod
    def rounded_number(cls, number: float) -> float:
        """Round the given number to the decimal positions specified by DECIMAL_POSITIONS."""
        return round(number, DragInfo.DECIMAL_POSITIONS)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DragInfo):
            return False
        return (
            self.is_dragging == other.is_dragging and 
            self.is_dragging_node == other.is_dragging_node and 
            self.is_dragging_connection == other.is_dragging_connection and 
            self.is_dragging_viewport == other.is_dragging_viewport and 
            self.node_id == other.node_id and 
            self.output_name == other.output_name and
            self.input_name == other.input_name and
            self.start_x == other.start_x and 
            self.start_y == other.start_y and 
            self.offset_x == other.offset_x and 
            self.offset_y == other.offset_y and
            self.current_x == other.current_x and
            self.current_y == other.current_y
        )

    def __repr__(self) -> str:
        return f"DragInfo(is_dragging={self.is_dragging}, is_dragging_node={self.is_dragging_node}, is_dragging_connection={self.is_dragging_connection}, is_dragging_viewport={self.is_dragging_viewport}, node_id={self.node_id}, output_name={self.output_name}, input_name={self.input_name}, start_x={self.start_x}, start_y={self.start_y}, offset_x={self.offset_x}, offset_y={self.offset_y}, current_x={self.current_x}, current_y={self.current_y})"

    def __str__(self) -> str:
        """Return a JSON-like string representation of the object."""
        return json.dumps(self, default=vars)

    def copy(self) -> 'DragInfo':
        return DragInfo(
            is_dragging=self.is_dragging,
            is_dragging_node=self.is_dragging_node,
            is_dragging_connection=self.is_dragging_connection,
            is_dragging_viewport=self.is_dragging_viewport,
            node_id=self.node_id,
            output_name=self.output_name,
            input_name=self.input_name,
            start_x=self.start_x,
            start_y=self.start_y,
            offset_x=self.offset_x,
            offset_y=self.offset_y,
            current_x=self.current_x,
            current_y=self.current_y,
        )
    
    def get_hovered_rectangle(self, rects: Rectangles, nodes_data: DrawflowInfo) -> Optional[Tuple[str, str, str]]:
        deleted = []
        match = None
        for (node_id, name, type), rect in rects._rects.items():
            if node_id in nodes_data._nodes:
                node = nodes_data[node_id]
                left = node.pos_x + rect.offset_left
                top = node.pos_y + rect.offset_top
                right = left + rect.width
                bottom = top + rect.height
                if left <= self.current_x <= right and top <= self.current_y <= bottom:
                    match = (node_id, name, type)
                    break
            else:
                deleted.append((node_id, name, type))
        [rects.delete_rectangle(node_id, name, type) for node_id, name, type in deleted]
        return match
