import numpy as np
import math


def genmap(length, x, y, x_spacing, y_spacing, first=0, x0=0, y0=0, top_left=False):
    markers = []
    max_y = y0 + (y - 1) * y_spacing
    for j in range(y):
        for i in range(x):
            pos_y = y0 + j * y_spacing
            if top_left:
                pos_y = max_y - pos_y
            markers.append(
                {"id": first, "length": length, "x": x0 + x_spacing * i, "y": pos_y, "z": 0, "rot_x": 0,
                 "rot_y": 0, "rot_z": 0})
            first += 1
    return markers


def translate_map(map, dx=0, dy=0, dz=0):
    newmap = []
    for marker in map:
        marker["x"] += dx
        marker["y"] += dy
        marker["z"] += dz
        newmap.append(marker)
    return newmap


def rotate_map_z(map, angle, x0=0, y0=0, center=False):
    if center:
        for marker in map:
            x0 += marker["x"]
            y0 += marker["y"]
        x0 /= len(map)
        y0 /= len(map)
    newmap = []
    for marker in map:
        x = marker["x"] - x0
        y = marker["y"] - y0
        marker["x"] = x0 + x * math.cos(angle) - y * math.sin(angle)
        marker["y"] = y0 + x * math.sin(angle) + y * math.cos(angle)
        marker["rot_z"] += angle
        newmap.append(marker)
    return newmap


def print_map(map):
    print('# id\tlength\tx\ty\tz\trot_z\trot_y\trot_x')
    for marker in map:
        print('{}\t{}\t{:0.2f}\t{:0.2f}\t{:0.2f}\t{}\t{}\t{}'.format(marker["id"], marker["length"], marker["x"], marker["y"],
                                                      marker["z"], marker["rot_z"], marker["rot_y"], marker["rot_x"]))


def exclude_17(map):
    newmap = []
    for marker in map:
        if marker["id"] != 17:
            newmap.append(marker)
    return newmap

if __name__ == '__main__':
    map1 = genmap(0.22, 3, 10, 0.28, 0.28, top_left= True)
    map2 = genmap(0.22, 3, 10, 0.28, 0.28, first=30, top_left= True)
    map2 = rotate_map_z(map2, math.radians(180), center=True)
    map2 = translate_map(map2, dx=0.28 * 3)
    map1.extend(map2)

    print_map(exclude_17(map1))
