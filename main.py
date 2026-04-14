from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from src.line_of_sight import compute_line_of_sight_map


def main():
    img = Image.open("output/topologie/n47_e009_1arc_v3.tif")
    topology = np.array(img)

    position = (47.198217, 9.305193)
    target = (47.155526, 9.312698)


    result = compute_line_of_sight_map(topology, position, target)

    distance = []
    height = []
    colors = []

    for c in result.values():
        distance.append(c.distance)
        height.append(c.height)
        colors.append('green' if c.is_in_sight[0] else 'red')

    plt.figure(figsize=(10, 5))
    plt.scatter(distance, height, c=colors)
    plt.plot(distance, height)
    plt.grid()

    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title('Line of Sight Profile')
    #plt.gca().set_aspect('equal', adjustable='box')

    plt.show()


if __name__ == "__main__":
    main()