from typing import Dict, Any, Optional, Tuple

from reactpy import component, html, event

from GeometryProxy import Rect
from drawflow_logger import log
from NodeInfo import NodeInfo
from ConnectionInfo import ConnectionInfo
from DrawflowInfo import DrawflowInfo
from Rectangles import Rectangles

@component
def Connections(nodes_data: DrawflowInfo, rects: Rectangles, selected_connection: Optional[ConnectionInfo], set_selected_connection: Any, set_selected_node: Any, drag_data: Any):        
    hovered_port = drag_data.get_hovered_rectangle(rects, nodes_data)
    
    def calculate_node_position(node_id: str, port_id: str, type: str) -> Tuple[float, float]:
        log(f"Connections.calculate_node_position")
        connection_rect = rects.get_rectangle(node_id, port_id, type) or Rect()
        node_data = nodes_data._nodes[node_id]
        pos_x = node_data.pos_x + connection_rect.offset_left + connection_rect.width / 2
        pos_y = node_data.pos_y + connection_rect.offset_top + connection_rect.height / 2
        return (pos_x, pos_y)
    
    def draw_connection(start_pos: Tuple[float, float], end_pos: Tuple[float, float], connection_data: Optional[ConnectionInfo] = None) -> Any:
        log(f"Connections.draw_connection")
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        # Distance between the start and end points
        distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
    
        # Control points calculation
        control_point_offset = min(200, distance / 2)  # Limit maximum control point distance
        control_x1 = start_x + control_point_offset
        control_y1 = start_y
        control_x2 = end_x - control_point_offset
        control_y2 = end_y
    
        # Create a cubic Bézier path between two points with control points
        path_data = f"M {start_x},{start_y} C {control_x1},{control_y1} {control_x2},{control_y2} {end_x},{end_y}"
        
        path = html.make_vdom_constructor("path")
        if connection_data:
            @event(prevent_default=True, stop_propagation=True)
            def on_connection_click(event):
                set_selected_connection(connection_data)
                set_selected_node(None)

            connection_classes = "main-path"
            custom_styles = {}
            if selected_connection == connection_data:
                connection_classes += " selected"
            elif hovered_port and connection_data.node == hovered_port[0] and connection_data.input == hovered_port[1] and not hovered_port[0] == drag_data.node_id:
                custom_styles = {"stroke": "#ff4e4e97"}

            return path(
                {"d": path_data, "class_name": connection_classes, "onMouseDown": on_connection_click, "style": custom_styles},
            )
        else:
            if hovered_port and hovered_port[0] == drag_data.node_id:
                custom_styles = {"stroke": "#ff4e4e97"}
            else:
                custom_styles = {}
            return path({"d": path_data, "class_name": "main-path selected", "style": custom_styles})
    
    def render_connections() -> list:
        log(f"Connections.render_connections")
        connections = []
        for emitter_node_id, emitter_node_data in nodes_data._nodes.items():
            for output_port_key, output_data in emitter_node_data.outputs.items():
                for connection in output_data.connections:
                    receiver_node_id = connection.node
                    receiver_node_port = connection.input
                    start_pos = calculate_node_position(emitter_node_id, output_port_key, "output")
                    end_pos = calculate_node_position(receiver_node_id, receiver_node_port, "input")

                    connections.append(draw_connection(start_pos, end_pos, connection))
        
        if drag_data.is_dragging_connection:
            start_pos = calculate_node_position(drag_data.node_id, drag_data.output_name, "output")
            end_pos = (drag_data.current_x, drag_data.current_y)
            connections.append(draw_connection(start_pos, end_pos))
        
        return connections
    
    log(f'Connections ➜ 🖼 {nodes_data._nodes.keys()}')
    
    return html.svg({"class_name": "connection"}, render_connections())
