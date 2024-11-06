import yaml
import xml.etree.ElementTree as ET

def addel(arr, xml, path=""):
    clss = xml.tag

    el = {}

    if clss != "Score":
        el["Parent"] = path if path != "" else "Score"

    for name, value in xml.attrib.items():
        if value == "":
            continue

        if name == "Name":
            value = value.replace(" ", "")
        elif clss == "Instr" and name == "Partiture":
            value = "_" + value

        el[name] = value

    Id = f"{path}_{el["Name"]}" if clss != "Score" else "Score"
    el["Id"] = Id

    for xitem in xml:
        if xitem.tag == "Note":
            continue

        addel(arr, xitem, Id if clss != "Score" else "")

    arr.insert(0, {clss: [el]})

filename = "C:\\Code\\p.Music\\128\\128.Score"
xml = ET.parse(filename).getroot()

arr = []
addel(arr, xml)

yamlname = filename.replace(".Score", ".graph.yaml")
with open(yamlname, 'w') as file:
    yaml.dump(arr, file, default_flow_style=False, allow_unicode=True)
