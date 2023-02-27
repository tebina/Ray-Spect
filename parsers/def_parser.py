from utils.utils import remove_backslashes


def extract_data(line):
    line = line.lstrip("- ")
    s = line.split(" ")
    component_tuple = s[0].split("/") + [s[1]]
    coordinates_tuple = line.split("(")[1].split(" ")[1:3]
    return component_tuple, coordinates_tuple


def get_die_area(line):
    return [line.split(" ")[2], line.split(" ")[3]], [line.split(" ")[6], line.split(" ")[7]]


class DefParser:
    def __init__(self, def_file, region_point1, region_point2):
        um = 1e3
        self.def_file = def_file
        self.xcoord1 = region_point1[0] * um
        self.xcoord2 = region_point2[0] * um
        self.ycoord1 = region_point1[1] * um
        self.ycoord2 = region_point2[1] * um
        self.die_area = 0
        self.components_data = []

    def __del__(self):
        return

    def prepare_data(self):
        raw_strings = []
        with open(self.def_file, 'r') as f:
            for line in f:
                if line.split(" ")[0] == "COMPONENTS":
                    for line in f:
                        if line == " ;\n":
                            continue
                        if line == "END COMPONENTS\n":
                            break
                        raw_strings.append(line)
                if line.split(" ")[0] == "DIEAREA":
                    self.die_area = get_die_area(line)
        return raw_strings

    def def_parser(self):
        raw_strings = self.prepare_data()
        for raw_string in raw_strings:
            if "FILLER" in raw_string:
                continue
            mydict = {}
            extracted_data = extract_data(raw_string)
            extracted_data[0][0] = remove_backslashes(extracted_data[0][0])
            mydict["instance"] = extracted_data[0]
            mydict["xcoord"] = extracted_data[1][0]
            mydict["ycoord"] = extracted_data[1][1]
            self.components_data.append(mydict)
        return self.components_data

    def region_fetch(self):
        """
        fetch all instances inside a region

        :return: list of instances inside a region
        """
        all_instances = self.def_parser()
        um = 1e3
        instances_in_region = []
        # plt.figure(figsize=(20, 20), dpi=200)
        for instance in all_instances:
            if self.xcoord1 < int(instance["xcoord"]) < self.xcoord2 and self.ycoord1 < int(
                    instance["ycoord"]) < self.ycoord2:
                instances_in_region.append(instance["instance"])
        #         plt.plot(float(instance["xcoord"]) / um, float(instance["ycoord"]) / um, marker="s", markersize=10,
        #                  markeredgecolor="yellow", markerfacecolor="red")
        #         plt.text(float(instance["xcoord"]) / um, float(instance["ycoord"]) / um, instance["instance"][-2],
        #                  rotation=45, fontsize=5, weight='bold')
        #     else:
        #         plt.plot(float(instance["xcoord"]) / um, float(instance["ycoord"]) / um, marker="s", markersize=10,
        #                  markeredgecolor="yellow", markerfacecolor="blue")
        # plt.savefig("instance_region.pdf", dpi='figure')
        print("There are", len(instances_in_region), "instances in the rectangle in micrometers : (", self.xcoord1/um,
              ",",
              self.ycoord1/um, ") (", self.xcoord2/um, ",", self.ycoord2/um, ")")
        return instances_in_region
