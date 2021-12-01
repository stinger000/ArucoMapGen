import math


def genmap(length, x, y, x_spacing, y_spacing, first=0, x0=0, y0=0, top_left=False):
    '''
    Generate map of ArUco markers
    :param length: length of marker
    :param x: number of markers by x
    :param y: number of markers by y
    :param x_spacing: distance between markers by x
    :param y_spacing: distance between markers by y
    :param first: first marker id
    :param x0: firs marker x coordinate
    :param y0: first marker y coordinate
    :param top_left: generate map by top left corner
    :return: list of ArUco markers
    '''
    markers = []
    for j in range(y):
        for i in range(x):
            pos_y = y0 + j * y_spacing
            if top_left:
                pos_y = y0 - j * y_spacing
            markers.append(
                {"id": first, "length": length, "x": x0 + x_spacing * i, "y": pos_y, "z": 0, "rot_x": 0,
                 "rot_y": 0, "rot_z": 0})
            first += 1
    return markers


def translate_map(map, dx=0, dy=0, dz=0):
    '''
    Translate map along each axis
    :param map: list of markers
    :param dx: x distance
    :param dy: y distance
    :param dz: x distance
    :return: list of translated markers
    '''
    newmap = []
    for marker in map:
        marker["x"] += dx
        marker["y"] += dy
        marker["z"] += dz
        newmap.append(marker)
    return newmap


def rotate_map_z(map, angle, x0=0, y0=0, center=False):
    '''
    Rotate map around z axis
    :param map: list of markers
    :param angle: rotation angle
    :param x0: center point x coordinate
    :param y0: center point y coordinate
    :param center: if True, rotate around map center
    :return: list of rotated markers
    '''
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
    '''
    Print map to standard output
    :param map: list of markers
    '''
    print('# id\tlength\tx\ty\tz\trot_z\trot_y\trot_x')
    for marker in map:
        print('{}\t{}\t{:0.2f}\t{:0.2f}\t{:0.2f}\t{}\t{}\t{}'.format(marker["id"], marker["length"], marker["x"],
                                                                     marker["y"],
                                                                     marker["z"], marker["rot_z"], marker["rot_y"],
                                                                     marker["rot_x"]))


def exclude_17(map):
    '''
    Delete 17 marker from map
    :param map: original list of markers
    :return: list of markers
    '''
    newmap = []
    for marker in map:
        if marker["id"] != 17:
            newmap.append(marker)
    return newmap

def concatenate_maps(*args):
    map = []
    for m in args:
        map.extend(m)
    return map


if __name__ == '__main__':
    map1 = genmap(0.22, 3, 10, 0.28, 0.28, top_left=True)
    map2 = genmap(0.22, 3, 10, 0.28, 0.28, first=30, top_left=True)
    map2 = rotate_map_z(map2, math.radians(180), center=True)
    map2 = translate_map(map2, dx=0.28 * 3)
    # map1.extend(map2)
    map = concatenate_maps(map1, map2)

    print_map(exclude_17(map))
