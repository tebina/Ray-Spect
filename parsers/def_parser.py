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
    return raw_strings


def def_parser(def_file):
    components_data = []
    raw_strings = prepare_data(def_file)
    for raw_string in raw_strings:
        components_data.append(extract_data(raw_string))
    return components_data


