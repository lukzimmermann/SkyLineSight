from dataclasses import dataclass

import numpy as np


@dataclass
class CoordinatePoint:
    x: int
    y: int
    height: float
    is_in_sight: list[bool]
    distance: float

class LineOfSight():
    def __init__(self):
        pass

    def compute_line_of_sight_map(
        self,
        topology_map: np.ndarray,
        position_latlon: tuple[float, float],
        height_offset: float = 1.8
    ):
        coordinates = {}

        boarder_indexes = self.get_border_indexes(topology_map.shape)

        for index in boarder_indexes:
            pos_x, pos_y = self._latlon_to_pixel(*position_latlon, topology_map.shape)
            tgt_x, tgt_y = index
            
            max_angle = -np.inf

            points = self._bresenham_line(pos_x, pos_y, tgt_x, tgt_y)

            base_height = topology_map[pos_y, pos_x] + height_offset

            for x, y in points:
                if (x, y) in coordinates:
                    continue

                dx = x - pos_x
                dy = y - pos_y

                distance = self._pixel_distance_to_meters(dx, dy, position_latlon[0])

                height_diff = topology_map[y, x] - base_height

                angle = np.arctan2(height_diff, distance if distance != 0 else 1e-6)

                is_visible = angle >= max_angle

                if is_visible:
                    max_angle = angle

                coordinates[(x, y)] = CoordinatePoint(
                    x=x,
                    y=y,
                    height=float(topology_map[y, x]),
                    is_in_sight=[is_visible],
                    distance=float(distance)
                )

        return coordinates

    def compute_line_of_sight_line(
        self,
        topology_map: np.ndarray,
        position_latlon: tuple[float, float],
        target_latlon: tuple[float, float],
        height_offset: float = 1.8
    ):
        pos_x, pos_y = self._latlon_to_pixel(*position_latlon, topology_map.shape)
        tgt_x, tgt_y = self._latlon_to_pixel(*target_latlon, topology_map.shape)

        coordinates = {}
        max_angle = -np.inf

        points = self._bresenham_line(pos_x, pos_y, tgt_x, tgt_y)

        base_height = topology_map[pos_y, pos_x] + height_offset

        for x, y in points:
            dx = x - pos_x
            dy = y - pos_y

            distance = self._pixel_distance_to_meters(dx, dy, position_latlon[0])

            height_diff = topology_map[y, x] - base_height

            angle = np.arctan2(height_diff, distance if distance != 0 else 1e-6)

            is_visible = angle >= max_angle

            if is_visible:
                max_angle = angle

            coordinates[(x, y)] = CoordinatePoint(
                x=x,
                y=y,
                height=float(topology_map[y, x]),
                is_in_sight=[is_visible],
                distance=float(distance)
            )

        return coordinates


    def _bresenham_line(self, x0, y0, x1, y1):
        points = []

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        x, y = x0, y0

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        if dx > dy:
            err = dx / 2.0
            while x != x1:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

        points.append((x1, y1))
        return points

    def _latlon_to_pixel(self, lat, lon, shape):
        height, width = shape
    
        lat_min, lat_max = 47.0, 48.0
        lon_min, lon_max = 9.0, 10.0
    
        x = int((lon - lon_min) / (lon_max - lon_min) * (width - 1))
        y = int((lat_max - lat) / (lat_max - lat_min) * (height - 1))
    
        return x, y  
    
    def _pixel_distance_to_meters(self, dx, dy, lat):
        meters_per_lat = 111320 / 3600  # ~30.92 m per pixel (north-south)
    
        meters_per_lon = (111320 * np.cos(np.radians(lat))) / 3600
    
        dx_m = dx * meters_per_lon
        dy_m = dy * meters_per_lat
    
        return np.sqrt(dx_m**2 + dy_m**2)
    
    def get_border_indexes(self, shape: tuple[int, int]) -> list[tuple[int, int]]:
        rows, cols = shape
        border = []
    
        for x in range(rows):
            for y in range(cols):
                if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
                    border.append((x, y))
    
        return border