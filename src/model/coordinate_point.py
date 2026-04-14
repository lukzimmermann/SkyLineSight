from dataclasses import dataclass

@dataclass
class CoordinatePoint:
    x: int
    y: int
    height: int
    is_in_sight: list[bool]
    distance: float