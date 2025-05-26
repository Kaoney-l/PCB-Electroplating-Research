"""
Sub-board images for generating boundaries
"""
from PIL import Image, ImageDraw
import csv
import math
from Utils import y_value

def read_coordinates(filename):
    extreme_coordinates = []

    with open(filename, 'r') as file:
        for line in file:
            # Extract coordinate information from each line
            values = line.strip().split()
            # Converts a string to a floating point number and adds it to the list of coordinates
            max_x, max_y, min_x, min_y = map(float, values)
            extreme_coordinates.append((max_x, max_y, min_x, min_y))

    return extreme_coordinates


def point_in_range(point, range):
    x, y = point
    max_x, max_y, min_x, min_y = range
    if min_x <= x <= max_x and min_y <= y <= max_y:
        return True
    return False


# Scaling coordinates to image size
def scale_coord(x, y, m_in_sf):
    max_x, max_y, min_x, min_y = m_in_sf
    scaled_x = int((x - min_x) * width / (max_x - min_x))
    scaled_y = int((y - min_y) * height / (max_y - min_y))
    return scaled_x, scaled_y



for u in range(1,2):
    pad_file_path = r'data/surface.txt'
    sc_set = []
    # Read a file and extract data starting with 'A'

    sliding_scale = 1000
    line_size = 4

    # Reading coordinates from coordinates.txt file
    extreme_coordinates = read_coordinates('sfcoordinates.txt')


    # Circular Arc Data
    arc_in_sfs = [[] for _ in extreme_coordinates]
    sc_arc_in_sfs = [[] for _ in extreme_coordinates]

    # Linear data
    l_in_sfs = [[] for _ in extreme_coordinates]
    sc_l_in_sfs = [[] for _ in extreme_coordinates]

    # pad data
    pad_in_sfs = [[] for _ in extreme_coordinates]
    sc_pad_in_sfs = [[] for _ in extreme_coordinates]



    arc_data = None
    # polygonal starting point
    start_point = None
    with open(pad_file_path, 'r') as file:
        for line in file:
            if line.startswith('A'):
                arc_data = line.split()[1:7]  # Extract data
                arc_data = [float(x) for x in arc_data]  # Convert data to floating point numbers

                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range([arc_data[0], arc_data[1]], extreme_coordinate):
                        arc_in_sfs[i].append(arc_data)

                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)

                        x1, y1 = scale_coord(arc_data[0], arc_data[1], extreme_coordinate)
                        x2, y2 = scale_coord(arc_data[2], arc_data[3], extreme_coordinate)
                        x3, y3 = scale_coord(arc_data[4], arc_data[5], extreme_coordinate)
                        y1 = height - y1
                        y2 = height - y2
                        y3 = height - y3
                        sc_arc_in_sfs[i].append([x1, y1, x2, y2, x3, y3])

            if line.startswith('L'):
                # Extract the starting coordinates of the line
                coordinates = line.split()[1:5]  
                # Convert coordinates to floating point numbers
                coordinates = [float(coord) for coord in coordinates]

                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range([coordinates[0], coordinates[1]], extreme_coordinate):
                        l_in_sfs[i].append(coordinates)

                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)

                        x1, y1 = scale_coord(coordinates[0], coordinates[1], extreme_coordinate)
                        x2, y2 = scale_coord(coordinates[2], coordinates[3], extreme_coordinate)
                        y1 = height - y1
                        y2 = height - y2
                        sc_l_in_sfs[i].append([x1, y1, x2, y2])



            if line.startswith('P'):
                # Extract the coordinates of the circle
                coordinates = line.split()[1:3]  
                coordinates = [float(coord) for coord in coordinates]
                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range([coordinates[0], coordinates[1]], extreme_coordinate):
                        pad_in_sfs[i].append(coordinates)
                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)
                        x1, y1 = scale_coord(coordinates[0], coordinates[1], extreme_coordinate)
                        y1 = height - y1
                        sc_pad_in_sfs[i].append([x1, y1])



    with open(pad_file_path, 'r') as file:
        for line in file:
            tokens = line.strip().split()
            if line.startswith('OB'):
                start_point = (float(tokens[1]), float(tokens[2]))
            elif line.startswith('OS'):
                end_point = (float(tokens[1]), float(tokens[2]))
                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range(start_point, extreme_coordinate):
                        l_in_sfs[i].append((start_point, end_point))

                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)
                        x1, y1 = scale_coord(start_point[0], start_point[1], extreme_coordinate)
                        x2, y2 = scale_coord(end_point[0], end_point[1], extreme_coordinate)
                        y1 = height - y1
                        y2 = height - y2
                        sc_l_in_sfs[i].append([x1, y1, x2, y2])


                start_point = end_point
            elif line.startswith('OC'):
                end_point = (float(tokens[1]), float(tokens[2]))
                center_point = (float(tokens[3]), float(tokens[4]))
                for i, extreme_coordinate in enumerate(extreme_coordinates):
                    if point_in_range(start_point, extreme_coordinate):
                        arc_in_sfs[i].append([start_point[0], start_point[1], end_point[0], end_point[1], center_point[0], center_point[1]])


                        width = int((extreme_coordinate[0] - extreme_coordinate[2]) * sliding_scale)
                        height = int((extreme_coordinate[1] - extreme_coordinate[3]) * sliding_scale)

                        x1, y1 = scale_coord(start_point[0], start_point[1], extreme_coordinate)
                        x2, y2 = scale_coord(end_point[0], end_point[1], extreme_coordinate)
                        x3, y3 = scale_coord(center_point[0], center_point[1], extreme_coordinate)
                        y1 = height - y1
                        y2 = height - y2
                        y3 = height - y3
                        sc_arc_in_sfs[i].append([x1, y1, x2, y2, x3, y3])

                start_point = end_point

    # Print results
    em_datas = []
    for i, sc_arc_in_sf in enumerate(sc_arc_in_sfs):
        sc_l_in_sf = sc_l_in_sfs[i]
        sc_pad_in_sf = sc_pad_in_sfs[i]

        if len(sc_arc_in_sf) == 0 or len(sc_l_in_sf) == 0:
            continue
        width = int((extreme_coordinates[i][0] - extreme_coordinates[i][2]) * sliding_scale)
        height = int((extreme_coordinates[i][1] - extreme_coordinates[i][3]) * sliding_scale)
        # if width != 159:
        #     continue
        image = Image.new("RGB", (width, height), "white")
        x = 0
        if x == 0:
            draw = ImageDraw.Draw(image)

            for sc_arc in sc_arc_in_sf:
                x1, y1, x2, y2, x3, y3 = sc_arc

                # Calculate center and radius of the circle
                cx = x3
                cy = y3
                radius = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)
                # Calculate start and end angles
                start_angle = math.atan2(y1 - cy, x1 - cx)
                end_angle = math.atan2(y2 - cy, x2 - cx)
                # Convert angles to degrees
                start_angle = math.degrees(start_angle)
                end_angle = math.degrees(end_angle)
                # Ensure end angle is greater than start angle
                if start_angle > end_angle:
                    end_angle += 360

                # PIL's arc function requires angles in the format (start, end)
                # where 0 degrees is at the 3 o'clock position
                draw.arc((cx - radius, cy - radius, cx + radius, cy + radius), start=start_angle, end=end_angle, fill="black",
                        width=line_size)


            for sc_line in sc_l_in_sf:
                x1, y1, x2, y2 = sc_line
                draw.line([(x1, y1), (x2, y2)], fill="black", width=line_size)


            for sc_pad in sc_pad_in_sf:
                x, y = sc_pad
                radius = line_size  
                draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], outline="black")

        image.save("data/image/data" + str(u) + "/output_" + str(i) +"x"+ ".png")


    file_name = "em_data.txt"
    em_datas = []
    max_num = 0

    for i, arc_in_sf in enumerate(arc_in_sfs):
        num = 0
        l_in_sf = l_in_sfs[i]
        pad_in_sf = pad_in_sfs[i]
        # if len(arc_in_sf) == 0 and len(l_in_sf) == 0 and len(pad_in_sf) == 0:
        #     continue
        width = int((extreme_coordinates[i][0] - extreme_coordinates[i][2]) * sliding_scale)
        height = int((extreme_coordinates[i][1] - extreme_coordinates[i][3]) * sliding_scale)
        print(width)
        if 159 == 159:
            em_data = []
            # for arc in arc_in_sf:
            #     num += 1
            #     print(arc)
            #     x1, y1, x2, y2, x3, y3 = arc
            #     em_data.append(x1)
            #     em_data.append(y1)
            #     break
            # if num==1:
            #     break
            # for line in l_in_sf:
            #     num += 1
            #     x1, y1, x2, y2 = line
            #     em_data.append(2)
            #     em_data.append(x1)
            #     em_data.append(y1)
            #     break
            # if num == 1:
            #     break
            for pad in pad_in_sf:
                num += 1
                x1, y1 = pad
                em_data.append(x1)
                em_data.append(y1)
                break
            em_datas.append(em_data)
            # if num < 60:
            #     for i in range(60-num):
            #         for j in range(7):
            #             em_data.append(0)


    with open('.\dataset\em_train_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(em_datas)
    # with open('result/Arc_sc.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['X1', 'Y1', 'X2', 'Y2','X3', 'Y3', 'X1-sc', 'Y1-sc', 'X2-sc', 'Y2-sc','X3-sc', 'Y3-sc'])  # 写入标题行
    #     for row in sc_set:
    #         writer.writerow(row)
