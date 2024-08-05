from typing import Any, Dict, Tuple

from reactpy import component, use_state, html, event

from Connections import Connections
from GeometryProxy import GeometryProxy, Rect
from DragInfo import DragInfo
from DrawflowInfo import DrawflowInfo
from drawflow_logger import log
from ConnectionInfo import ConnectionInfo
from Rectangles import Rectangles

@component
def Drawflow(nodes_data: DrawflowInfo, set_nodes_data: Any, component_map: Dict[str, Any], *, _offset: Tuple[float, float] = (0,0)):
    MOUSE_POINTER_OFFSET_X = _offset[0]
    MOUSE_POINTER_OFFSET_Y = _offset[1]
    CANVAS_DEFAULT_WIDTH = 500
    CANVAS_DEFAULT_HEIGHT = 500
    CANVAS_GROWTH_MARGIN = 200  # Distance from the edge to trigger canvas expansion
    CANVAS_GROWTH_STEP = 200  # Amount to increase the canvas size by
    LEFT_MOUSE_BUTTON_INDEX = 0
    
    drag_data, set_drag_data = use_state(DragInfo())
    selected_node, set_selected_node = use_state(None)
    selected_connection, set_selected_connection = use_state(None)
    rects, set_rects = use_state(Rectangles())

    canvas_width, set_canvas_width = use_state(CANVAS_DEFAULT_WIDTH)
    canvas_height, set_canvas_height = use_state(CANVAS_DEFAULT_HEIGHT)
    viewport_x, set_viewport_x = use_state(0)
    viewport_y, set_viewport_y = use_state(0)

    @event(prevent_default=True, stop_propagation=True)
    def on_mouse_move(event):
        log(f"Drawflow.on_mouse_move")
        
        if not drag_data.is_dragging:
            return
        
        if event.get("buttons", 0) == 0 or event.get("button", -1) != LEFT_MOUSE_BUTTON_INDEX:
            # Mouse was released, but we missed the event
            set_drag_data(DragInfo())
            return
        
        client_x = event.get("clientX", 0)
        client_y = event.get("clientY", 0)

        drag_data.current_x = client_x - MOUSE_POINTER_OFFSET_X - viewport_x
        drag_data.current_y = client_y - MOUSE_POINTER_OFFSET_Y - viewport_y
        set_drag_data(drag_data.copy())

        if drag_data.is_dragging_viewport:
            new_x = client_x - drag_data.offset_x
            new_y = client_y - drag_data.offset_y
            set_viewport_x(new_x)
            set_viewport_y(new_y)
            
        elif drag_data.is_dragging_node:
            node_id = drag_data.node_id
            new_x = client_x - drag_data.offset_x
            new_y = client_y - drag_data.offset_y
            nodes_data[node_id].pos_x = new_x
            nodes_data[node_id].pos_y = new_y
            set_nodes_data(nodes_data.copy())
        
    @event(prevent_default=True, stop_propagation=True)
    def on_mouse_up(event):
        log(f"Drawflow.on_mouse_up")
        if drag_data.is_dragging_connection:
            hovered_rectangle = drag_data.get_hovered_rectangle(rects, nodes_data)
            if hovered_rectangle and hovered_rectangle[0] != drag_data.node_id:
                receiver_node_id, receiver_port_name, receiver_type = hovered_rectangle
                if receiver_type == "input":
                    # Remove any existing connections to this input
                    for other_node_id, other_node_data in nodes_data._nodes.items():
                        for output_name, output_data in other_node_data.outputs.items():
                            connections = output_data.connections
                            for connection in connections:
                                if connection.node == receiver_node_id and connection.input == receiver_port_name:
                                    connections.remove(connection)
                                    set_nodes_data(nodes_data.copy())
                                    break
                    # Add the new connection
                    if receiver_port_name not in nodes_data[drag_data.node_id].outputs:
                        nodes_data[drag_data.node_id].outputs[drag_data.output_name].connections.append(ConnectionInfo(node=receiver_node_id, input=receiver_port_name))
                        set_nodes_data(nodes_data.copy())
        
        else:
            set_drag_data(DragInfo())

    @event(prevent_default=True, stop_propagation=True)
    def on_mouse_over_node(event):
        log(f"Drawflow.on_mouse_over_node")
        if not drag_data.is_dragging:
            start_x = event.get("clientX", 0)
            start_y = event.get("clientY", 0)
            THRESHOLD = 10
            is_beyond_threshold = (abs(start_x - drag_data.start_x) > THRESHOLD or abs(start_y - drag_data.start_y) > THRESHOLD)
            if is_beyond_threshold:
                set_drag_data(DragInfo())

    @event(prevent_default=True, stop_propagation=True)
    def on_delete_click(event):
        log(f"Drawflow.on_delete_click")
        if selected_node in nodes_data._nodes:
            # Remove deleted node
            nodes_data.remove(selected_node)
            # Remove connections pointing to the deleted node
            for node in nodes_data._nodes.values():
                for output in node.outputs.values():
                    for connection in output.connections:
                        if connection.node == selected_node:
                            output.connections.remove(connection)
            set_nodes_data(nodes_data.copy())
        elif selected_connection:
            # Remove selected connection
            for node in nodes_data._nodes.values():
                for output in node.outputs.values():
                    if selected_connection in output.connections:
                        output.connections.remove(selected_connection)
            set_nodes_data(nodes_data.copy())
            set_selected_connection(None)
    
    def update_canvas_size():
        log(f"Drawflow.update_canvas_size")
        corrected_canvas_width = canvas_width
        corrected_canvas_height = canvas_height
        for node_id, node in nodes_data._nodes.items():
            if node.pos_x > corrected_canvas_width - CANVAS_GROWTH_MARGIN:
                corrected_canvas_width = max(corrected_canvas_width + CANVAS_GROWTH_STEP, node.pos_x + CANVAS_GROWTH_STEP)
            if node.pos_y > corrected_canvas_height - CANVAS_GROWTH_MARGIN:
                corrected_canvas_height = max(corrected_canvas_height + CANVAS_GROWTH_STEP, node.pos_y + CANVAS_GROWTH_STEP)
        set_canvas_width(corrected_canvas_width)
        set_canvas_height(corrected_canvas_height)
    
    def start_dragging_node_or_connection(node_id, client_x, client_y):
        log(f"Drawflow.start_dragging")
        output_name = drag_data.output_name
        if drag_data.input_name:
            for candidate_node_id, node in nodes_data._nodes.items():
                for candidate_output_name, output_data in node.outputs.items():
                    connections = output_data.connections
                    for connection in connections:
                        if connection.node == node_id and connection.input == drag_data.input_name:
                            connections.remove(connection)
                            node_id = candidate_node_id
                            output_name = candidate_output_name
                            set_nodes_data(nodes_data.copy())
                            break
        
        node = nodes_data[node_id]
        offset_x = client_x - node.pos_x
        offset_y = client_y - node.pos_y

        new_drag_data = DragInfo(
            is_dragging_node=(output_name is None),
            is_dragging_connection=(output_name is not None),
            node_id=node_id,
            output_name=output_name,
            start_x=client_x,
            start_y=client_y,
            offset_x=offset_x,
            offset_y=offset_y,
            current_x=client_x - MOUSE_POINTER_OFFSET_X - viewport_x,
            current_y=client_y - MOUSE_POINTER_OFFSET_Y - viewport_y,
        )
        set_drag_data(new_drag_data)

    @event(prevent_default=True, stop_propagation=True)
    def on_mouse_down_canvas(event):
        log("Drawflow.on_mouse_down_canvas")
        if event.get("button") == LEFT_MOUSE_BUTTON_INDEX:
            client_x = event.get("clientX", 0)
            client_y = event.get("clientY", 0)
            offset_x = client_x - viewport_x
            offset_y = client_y - viewport_y
            new_drag_data = DragInfo(
                is_dragging_viewport=True,
                start_x=client_x,
                start_y=client_x,
                offset_x=offset_x,
                offset_y=offset_y,
                current_x=client_x - MOUSE_POINTER_OFFSET_X - viewport_x,
                current_y=client_y - MOUSE_POINTER_OFFSET_Y - viewport_y,
            )
            set_drag_data(new_drag_data)

    def add_node(node_id: str, dataNode: Any) -> Any:
        log(f"Drawflow.add_node")
        custom_class = dataNode.custom_class
        component_name = dataNode.component
        pos_x = dataNode.pos_x
        pos_y = dataNode.pos_y

        # Get the ReactPy component based on the component name
        component = component_map.get(component_name, lambda data, set_data: html.div("Component not found"))

        def update_node(new_data):
            nodes_data[node_id].data = new_data
            set_nodes_data(nodes_data.copy())

        # Create node content with the selected component
        content = component(dataNode, update_node)

        # Create inputs and outputs containers
        
        def store_rect(key: str, type: str, rect: Any) -> None:
            log(f"Drawflow.add_node.store_rect")
            rects.add_rectangle(node_id, key, type, rect)
            set_rects(rects.copy())

        def on_mouse_over_input(event, input_name):
            log(f"Drawflow.add_node.on_mouse_over_input")
            if not drag_data.is_dragging:
                drag_data.node_id = node_id
                drag_data.input_name = input_name
                drag_data.start_x = event.get("clientX", 0)
                drag_data.start_y = event.get("clientY", 0)

        inputs = html.div(
            {"class_name": "inputs"},
            [
                html.div(
                    {
                        "class_name": f"input input_{index+1}",
                        "onMouseOver" : lambda event, input_name=input_name:
                            on_mouse_over_input(event, input_name),
                    },
                    GeometryProxy(
                        lambda rect, input_name=input_name:
                            store_rect(input_name, "input", rect),
                        proxy_id=f"{node_id} input_{index+1}",
                        observe_resizes=False,
                    )
                )
                for index, input_name in enumerate(dataNode.inputs)
            ]
        )
                
        def on_mouse_over_output(event, output_name):
            log(f"Drawflow.add_node.on_mouse_over_output")
            if not drag_data.is_dragging:
                drag_data.node_id = node_id
                drag_data.output_name = output_name
                drag_data.start_x = event.get("clientX", 0)
                drag_data.start_y = event.get("clientY", 0)
        
        outputs = html.div(
            {"class_name": "outputs"},
            [
                html.div(
                    {
                        "class_name": f"output output_{index+1}",
                        "onMouseOver" : lambda event, output_name=output_name:
                            on_mouse_over_output(event, output_name),
                    },
                    GeometryProxy(
                        lambda rect, output_name=output_name:
                            store_rect(output_name, "output", rect),
                        proxy_id=f"{node_id} output_{index+1}",
                        observe_resizes=False,
                    )
                )
                for index, output_name in enumerate(dataNode.outputs)
            ]
        )
        
        @event(prevent_default=False, stop_propagation=True)
        def on_mouse_down_node(event):
            log(f"Drawflow.add_node.on_mouse_down_node")
            if event.get("button", -1) == LEFT_MOUSE_BUTTON_INDEX:
                clientX = event.get("clientX", 0)
                clientY = event.get("clientY", 0)
                start_dragging_node_or_connection(node_id, clientX, clientY)
            set_selected_node(node_id)
            set_selected_connection(None)

        # Determine the class name, adding a 'selected' class if this is the selected node
        node_classes = f"drawflow-node {custom_class}"
        
        # Initially hidden delete button
        delete_box = html.div(
            {
                "class_name": "drawflow-delete-hidden",
                "hidden": "hidden",
            },
        )
        
        if selected_node == node_id:
            node_classes += " selected"  # Add a custom 'selected' class
            if not drag_data.is_dragging: # Show delete button only when not dragging
                delete_box = html.div(
                    {
                        "class_name": "drawflow-delete",
                        "onMouseDown": on_delete_click,
                        "style": {"position": "absolute", "top": -38, "right": -20, "cursor": "pointer"}
                    },
                    "x"
                )

        # Create the main node div
        node = html.div({
            "id": f"node-{node_id}",
            "class_name": node_classes,
            "style": {"top": f"{pos_y}px", "left": f"{pos_x}px"},
            "onMouseDown": on_mouse_down_node,
            "onMouseOver": on_mouse_over_node
        }, [inputs, content, outputs, delete_box])

        return node

    nodes_vdom = [add_node(node_id, node_data) for node_id, node_data in nodes_data._nodes.items()] + [
        Connections(
            nodes_data, 
            rects, 
            selected_connection, 
            set_selected_connection,
            set_selected_node,
            drag_data
        )
    ]
    
    update_canvas_size()

    log(f'Drawflow ➜ 🖼 {nodes_data._nodes.keys()}')

    return html.div(
        {
            "id": "drawflow",
            "class_name": "drawflow",
            "onMouseMove": on_mouse_move,
            "onMouseUp": on_mouse_up,
            "onMouseDown": on_mouse_down_canvas,
            "style": {
                "width": f"{canvas_width}px",
                "height": f"{canvas_height}px",
                "transform": f"translate({viewport_x}px, {viewport_y}px)"
            },
        },
        nodes_vdom
    )
