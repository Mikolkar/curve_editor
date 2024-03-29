import matplotlib.pyplot as plt
import numpy as np
from curves.de_casteljau import de_casteljau


def mult_minus_one(lst):
    return [-1 * number for number in lst]


def return_bezier_spline(x, y, u_len):
    t_values = np.linspace(0, 1, num=u_len)
    w = [1 for _ in range(len(x))]
    bezier_points = [de_casteljau(x, y, w, t) for t in t_values]

    x_values = [point[0] for point in bezier_points]
    y_values = [point[1] for point in bezier_points]

    return x_values, y_values


def parse_list(lst):
    result = []
    for number in lst:
        number = number.strip()
        if number[-1] == "]":
            number = number[:-1]
        result.append(float(number))
    return result


def parse_data(file_path):
    def append_to_dict(key, sub_key, value):
        parsed_data[key][sub_key] = value

    with open(file_path, "r") as file:
        data = file.readlines()

    parsed_data = {}
    current_key = None
    note = ["x", "y", "t"]
    index = 0
    for line in data:
        if line.startswith("#"):
            current_key = int(line.rstrip()[1:])
            parsed_data[current_key] = {
                "x": [],
                "y": [],
                "t": [],
            }
        else:
            values_str = line.rstrip("]\n").split("[")
            vals_cut = values_str[1:]
            if len(vals_cut) > 0 and vals_cut[0] != "#":
                res = vals_cut[0].split(", ")
                parsed = parse_list(res)
                append_to_dict(current_key, note[index], parsed)
                index += 1
                index %= 3

    return parsed_data


file_path = "splines/curve_data9.txt"
parsed_data = parse_data(file_path)

fig, ax = plt.subplots()

ax.set_aspect("equal", adjustable="box")

for key in parsed_data:
    x = parsed_data[key]["x"]
    y = parsed_data[key]["y"]
    t = parsed_data[key]["t"]
    t = len(t)

    points = return_bezier_spline(x, y, t)
    sx, sy = points[0], points[1]
    ax.plot(sx, sy, "r-", linewidth=3)

plt.show()
