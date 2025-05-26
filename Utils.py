import numpy as np
import matplotlib.pyplot as plt
import csv
from PIL import Image, ImageDraw

# Converting coordinate points and thickness values to pixel positions and colour values on an image
def map_to_image(data, width, height, min_thickness, max_thickness):
    image = Image.new('RGB', (width, height), (255, 255, 255))  
    draw = ImageDraw.Draw(image)

    for point in data:
        x, y, thickness = point
        if max_thickness - min_thickness==0:
            xx = 123
        color = int(255 * (1 - (thickness - min_thickness) / (max_thickness - min_thickness))) 
        draw.rectangle([x-2, y-2, x+2, y+2], fill=(color, 0, 0))  

    return image

def scale_coord(x, y, m_in_sf, width, height):
    max_x, max_y, min_x, min_y = m_in_sf
    scaled_x = int((x - min_x) * width / (max_x - min_x))
    scaled_y = int((y - min_y) * height / (max_y - min_y))
    return scaled_x, scaled_y


def read_coordinates(filename):
    extreme_coordinates = []

    with open(filename, 'r') as file:
        for line in file:
            values = line.strip().split()
            max_x, max_y, min_x, min_y = map(float, values)
            extreme_coordinates.append((max_x, max_y, min_x, min_y))

    return extreme_coordinates


def point_in_range(point, range):
    x, y = point
    max_x, max_y, min_x, min_y = range
    if min_x <= x <= max_x and min_y <= y <= max_y:
        return True
    return False


def y_value(data_path):
    x_coords = []
    y_coords = []
    thickness_values = []
    extreme_coordinates = read_coordinates('sfcoordinates.txt')

    y_in_range = [[] for _ in range(len(extreme_coordinates))]
    sc_y_in_range = [[] for _ in range(len(extreme_coordinates))]

    min_x = float("inf")
    max_x = float("-inf")
    min_y = float("inf")
    max_y = float("-inf")

    max_thickness = float("-inf")
    min_thickness = float("inf")


    with open(data_path, 'r', encoding='UTF-8') as file:
        for _ in range(8):
            next(file)

        for line in file:
            arc_data = line.split()[0:3]
            data = line.split()
            if len(data) != 3:
                continue
            x = float(data[0])
            y = float(data[1])
            thickness = float(data[2])


            if thickness>max_thickness:
                max_thickness = thickness
            if thickness<min_thickness:
                min_thickness = thickness


            for i, extreme_coordinate in enumerate(extreme_coordinates):
                if point_in_range([x, y], extreme_coordinate):
                    y_in_range.append([x, y, thickness])

                    width = int((extreme_coordinate[0] - extreme_coordinate[2]) * 500)
                    height = int((extreme_coordinate[1] - extreme_coordinate[3]) * 500)

                    x1, y1 = scale_coord(x, y, extreme_coordinate, width, height)
                    y1 = height - y1
                    sc_y_in_range[i].append([x1, y1, thickness])

            if min_x > x:
                min_x = x
            if max_x < x:
                max_x = x
            if min_y > y:
                min_y = y
            if max_y < y:
                max_y = y


    for i, data in enumerate(sc_y_in_range):
        if len(data) == 0:
            continue
        width = int((extreme_coordinates[i][0] - extreme_coordinates[i][2]) * 500)
        height = int((extreme_coordinates[i][1] - extreme_coordinates[i][3]) * 500)
        # print(width, height)

        heat_map = map_to_image(data, width, height, min_thickness, max_thickness)
        heat_map.save("y_datasets/output_" + str(i) + "y.png")

    y_data = []
    for i, data in enumerate(sc_y_in_range):
        width = int((extreme_coordinates[i][0] - extreme_coordinates[i][2]) * 500)
        if width == 399:
            values = [item[2] for item in data]
            average_values = sum(values) / len(values)
            y_data.append(average_values)
        else:
            y_data.append(0)
    return y_data




