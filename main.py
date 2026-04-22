import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from src.line_of_sight import LineOfSight


def main():
    img = Image.open("output/topologie/n47_e009_1arc_v3.tif")
    topology = np.array(img)

    position = (47.198217, 9.305193) # Unterwasser
    position = (47.249395, 9.343290) # Santis
    target = (47.155526, 9.312698)

    line_of_sight = LineOfSight()
    start = time.perf_counter()
    #result = line_of_sight.compute_line_of_sight_line(topology, position, target)
    result = line_of_sight.compute_line_of_sight_map(topology, position, height_offset=20)

    
    img = np.zeros((topology.shape[0], topology.shape[1], 3), dtype=np.uint8)
    print(f"Processing {len(result)} points for visualization...")
    print(f"Processing time: {time.perf_counter() - start:.2f} seconds")

    for entry in result.values():
        color = (0, 255, 0) if entry.is_in_sight[0] else (255, 0, 0)
        img[entry.y, entry.x] = color

    Image.fromarray(img).save("los_map.png")

    if False:

        plt.figure(figsize=(10, 10))
        plt.imshow(img)
        plt.title('Line of Sight Map (Green: Visible, Red: Not Visible)')
        plt.axis('off')
        plt.grid()
        plt.show()

    print(f"Total points: {len(result)}")

    distance = []
    height = []
    colors = []


    #for c in result.values():
    #    distance.append(c.distance)
    #    height.append(c.height)
    #    colors.append('green' if c.is_in_sight[0] else 'red')
#
    #plt.figure(figsize=(10, 5))
    #plt.scatter(distance, height, c=colors)
    #plt.plot(distance, height)
    #plt.grid()
#
    #plt.xlabel('Distance (m)')
    #plt.ylabel('Height (m)')
    #plt.title('Line of Sight Profile')
    ##plt.gca().set_aspect('equal', adjustable='box')
#
    #plt.show()


if __name__ == "__main__":
    main()