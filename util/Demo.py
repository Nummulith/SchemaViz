import yaml
import time

"""
SchemaViz Demo
Author: Pavel ERESKO
"""

from ObjectModelFramework import SchemaVizObjectModel


def out(line):
    print("\r" + line, end="", flush=True)

with open('./src/Classes.yaml', 'r') as file:
    classes = yaml.safe_load(file)

while True:
    out("Render...")
    # try:

    with open('./src/Demo.yaml', 'r') as file:
        settings = yaml.safe_load(file)

    filenames = settings["Articles"]
    all_data = []
    for filename in [s.strip() for s in filenames.split(',')]:
        with open(settings["RootPath"] + filename + '.yaml', 'r') as file:
            data = yaml.safe_load(file)
            all_data += data
    settings["all_data"] = all_data

    OM = SchemaVizObjectModel(classes, all_data)
    OM.fetch()

    draw = OM.html(None, settings["Articles"], settings["Engine"], settings["ReloadTime"], html_wrap=True)
    with open(settings["RootPath"] + settings["Articles"] + '.html', 'w') as file:
        file.write(draw)
        
    # except Exception as e:
    #     out("Error !!!")

    if settings["RenderLoop"] <= 0:
        break

    out("Sleep ...")
    time.sleep(settings["RenderLoop"])

out("Done  ...")
