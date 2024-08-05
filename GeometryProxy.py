import json
from typing import Callable, Optional
from uuid import uuid4

from reactpy import component, html, event
from drawflow_logger import log

class Rect:
    """A class representing a rectangle's dimensions and position."""
    
    DECIMAL_POSITIONS = 1

    def __init__(self, *, offset_left: float = 0, offset_top: float = 0, width: float = 0, height: float = 0):
        self.offset_left = Rect.rounded_number(offset_left)
        self.offset_top = Rect.rounded_number(offset_top)
        self.width = Rect.rounded_number(width)
        self.height = Rect.rounded_number(height)

    @classmethod
    def rounded_number(cls, number: float) -> float:
        """Round the given number to the decimal positions specified by DECIMAL_POSITIONS."""
        return round(number, Rect.DECIMAL_POSITIONS)

    @classmethod
    def from_dict(cls, data: dict) -> 'Rect':
        return cls(
            offset_left=Rect.rounded_number(data.get('offsetLeft', 0)),
            offset_top=Rect.rounded_number(data.get('offsetTop', 0)),
            width=Rect.rounded_number(data.get('width', 0)),
            height=Rect.rounded_number(data.get('height', 0)),
        )
    
    def to_dict(self) -> dict:
        return {
            "offsetLeft": self.offset_left,
            "offsetTop": self.offset_top,
            "width": self.width,
            "height": self.height
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rect):
            return False
        return (
            self.offset_left == other.offset_left and
            self.offset_top == other.offset_top and
            self.width == other.width and
            self.height == other.height
        )

    def __repr__(self) -> str:
        return (
            f"Rect(offset_left={self.offset_left}, offset_top={self.offset_top}, width={self.width}, height={self.height})"
        )

    def __str__(self) -> str:
        """Return a JSON-like string representation of the object."""
        return json.dumps(self, default=vars)
    
    def copy(self) -> 'Rect':
        return Rect(
            offset_left=self.offset_left,
            offset_top=self.offset_top,
            width=self.width,
            height=self.height
        )

@component
def GeometryProxy(
    set_value: Callable[[Rect], None], 
    default_value: Rect = Rect(),
    *, 
    proxy_id: str = str(uuid4()),
    target_id: Optional[str] = None,
    observe_resizes: bool = True
):
    """
    A ReactPy component for observing and reporting geometry changes of an element.

    Args:
        set_value (Callable[[Rect], None]): A callback function to set the new Rect value.
        default_value (Rect): The default Rect value. Defaults to a zeroed Rect object.
        proxy_id (str): A unique identifier for the GeometryProxy. Defaults to a random UUID.
        target_id (Optional[str]): The ID of the target element to observe. Defaults to None.
        observe_resizes (bool): Whether to observe resize events. Defaults to True.
    """

    @event
    def handle_event(event: dict):
        """
        Handle the resize event and update the Rect value.

        Args:
            event (dict): The event dictionary containing event data.
        """
        current_target = event.get('currentTarget')
        if current_target:
            rect_data = current_target.get("value", "{}")
            if rect_data:
                rect_dict = json.loads(rect_data)
                rect_obj = Rect.from_dict(rect_dict)
                if rect_obj != default_value:
                    set_value(rect_obj)
    
    if observe_resizes:
        script = f"""
        var element = document.getElementById('{proxy_id}');
        if (element) {{
            var container = document.getElementById('{target_id}') || element.parentElement;
            if (container) {{
                function updateRect() {{
                    const rect = container.getBoundingClientRect();
                    const json = JSON.stringify({{
                        offsetLeft: container.offsetLeft,
                        offsetTop: container.offsetTop,
                        width: rect.width,
                        height: rect.height
                    }});
                    element.value = json;
                    element.dispatchEvent(new Event('resize'));
                }}
                // Initial call
                updateRect();
                // Set up ResizeObserver
                var resizeObserver = new ResizeObserver(updateRect);
                resizeObserver.observe(container);
                // Cleanup observer on element removal
                element.addEventListener('remove', () => resizeObserver.disconnect());
                container.addEventListener('remove', () => resizeObserver.disconnect());
            }}
        }}
        """
    else:
        script = f"""
            var element = document.getElementById('{proxy_id}');
            if (element) {{
                var container = document.getElementById('{target_id}') || element.parentElement;
                if (container) {{
                    const rect = container.getBoundingClientRect();
                    const json = '{{"offsetLeft":' + container.offsetLeft + ',"offsetTop":' + container.offsetTop + ',"width":' + rect.width + ',"height":' + rect.height + '}}';
                    element.value = json;
                    var event = new Event('resize');
                    element.dispatchEvent(event);
                }}
           }}
        """
    
    log(f'GeometryProxy ➜ 🆔{proxy_id} 📐{repr(default_value)}')
        
    return html.button(
        { "id": proxy_id, "value": json.dumps(default_value, default=vars), "onresize": handle_event, "hidden": "hidden" },
        html.script(script)
    )
