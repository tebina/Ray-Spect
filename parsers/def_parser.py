import matplotlib.pyplot as plt
def extract_data(line):
    line = line.lstrip("- ")
    s = line.split(" ")
    component_tuple = s[0].split("/") + [s[1]]
    coordinates_tuple = line.split("(")[1].split(" ")[1:3]
    return component_tuple, coordinates_tuple


def prepare_data(file_string):
    raw_strings = []
    with open(file_string, 'r') as f:
        for line in f:
            if line.split(" ")[0] == "COMPONENTS":
                for line in f:
                    if line == " ;\n":
                        continue
                    if line == "END COMPONENTS\n":
                        break
                    raw_strings.append(line)
            if line.split(" ")[0] == "DIEAREA":
                die_area_coord = die_area(line)
    print(die_area_coord)
    return raw_strings


def def_parser(def_file):
    components_data = []
    raw_strings = prepare_data(def_file)
    for raw_string in raw_strings:
        if "FILLER" in raw_string:
            continue
        mydict = {}
        extracted_data = extract_data(raw_string)
        mydict["instance"] = extracted_data[0]
        mydict["xcoord"] = extracted_data[1][0]
        mydict["ycoord"] = extracted_data[1][1]
        components_data.append(mydict)
    return components_data


def region_fetch(def_file, rect_point1, rect_point2):
    """
    fetch all instances inside a region
    :param def_file:
    :param rect_point1: (X,Y) coordinates of the first point of the rectangle in um
    :param rect_point2: (X,Y) coordinates of the second point of the rectangle in um
    :return: list of instances
    """
    all_instances = def_parser(def_file)
    um = 1e3
    xcoord1 = rect_point1[0] * um
    xcoord2 = rect_point2[0] * um
    ycoord1 = rect_point1[1] * um
    ycoord2 = rect_point2[1] * um
    instances_in_region = []
    plt.figure(figsize=(20, 20), dpi=200)
    for instance in all_instances:
        if xcoord1 < int(instance["xcoord"]) < xcoord2 and ycoord1 < int(instance["ycoord"]) < ycoord2:
            instances_in_region.append(instance["instance"])
            plt.plot(float(instance["xcoord"])/um, float(instance["ycoord"])/um, marker="s", markersize=10, markeredgecolor="yellow", markerfacecolor="red")
            plt.text(float(instance["xcoord"])/um, float(instance["ycoord"])/um,instance["instance"][-2] , rotation=45, fontsize=5, weight='bold')
        else: plt.plot(float(instance["xcoord"])/um, float(instance["ycoord"])/um, marker="s", markersize=10, markeredgecolor="yellow", markerfacecolor="blue")
    plt.savefig("instance_region.pdf", dpi='figure')
    print("There are", len(instances_in_region), "instances in the rectangle in micrometers : (", rect_point1[0],",",rect_point1[1],") (", rect_point2[0],",",rect_point2[1],")")
    return instances_in_region


def die_area(line):
    return [line.split(" ")[2], line.split(" ")[3]], [line.split(" ")[6], line.split(" ")[7]]





