from typing import Dict, Tuple, List, Optional

class Rectangles:
    def __init__(self):
        self._rects: Dict[Tuple[str, str, str], Tuple[float, float, float, float]] = {}

    def add_rectangle(self, node_id: str, name: str, type: str, rect: Tuple[float, float, float, float]):
        key: Tuple[int, str] = (node_id, name, type)
        self._rects[key] = rect

    def get_rectangle(self, node_id: str, name: str, type: str) -> Optional[Tuple[float, float, float, float]]:
        key: Tuple[int, str] = (node_id, name, type)
        return self._rects.get(key, None)

    def delete_rectangle(self, node_id: str, name: str, type: str):
        key: Tuple[int, str] = (node_id, name, type)
        if key in self._rects:
            del self._rects[key]

    def __del__(self):
        self._rects.clear()
        
    def copy(self) -> 'Rectangles':
        copy = Rectangles()
        copy._rects = self._rects.copy()
        return copy
