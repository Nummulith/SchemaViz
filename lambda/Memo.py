"""
Memorize!
Author: Pavel ERESKO
"""

import yaml
import sys
import time

from ObjectModelFramework import *

# ROOTPATH = "C:\\Code\\p.Music\\127_Score\\"

class USAGE:
    VALUE = "VALUE"
    LIST  = "LIST"

class COLOR:
    ORANGE    = "#FFC18A"
    RED_DARK  = "#E76E6F"
    RED       = "#F29F9B"
    RED_LIGHT = "#FDD0C7"
    LILA      = "#f2c4f4"
    BLUE_LIGHT= "#f0f9ff"
    BLUE      = "#d7c1ff"
    BLUE_DARK = "#c19fff"
    CRIMSON   = "#F2B3BC"
    GREEN     = "#a9dfbf"

class MemoItem(ObjectModelItem):
    # Icon = "AWS"
    Color = COLOR.GREEN

    @classmethod
    def get_objects(cls, node = None):
        if node is None:
            return MemoObjectModel.DATA[cls.__name__]
        else:
            for obj in MemoItem.get_objects():
                if obj["Id"] == node:
                    return [obj]
            return []

    # def get_icon(self):
    #     icon = super().get_icon()
    #     return os.path.abspath(ROOTPATH + 'icons').replace("\\", "/") + "/" + icon + ".png"

class MemoObjectModel(ObjectModel):
    def addSections(self, merged_data, filenames, clss=None, ids=None):
        for filename in [s.strip() for s in filenames.split(',')]:
            with open(self.settings["RootPath"] + filename + '.yaml', 'r') as file:
                data = yaml.safe_load(file)
                for section in data:
                    for key, values in section.items():
                        if clss != None and key != clss:
                            continue
                        for val in values:
                            if ids != None and val["Id"] not in ids:
                                continue
                            if key in merged_data:
                                merged_data[key].append(val)
                            else:
                                merged_data[key] = [val]
    
    def make_static_fields(self, fields):
        @staticmethod
        def static_fields():
            return fields
        return static_fields

    def __init__(self, clscfgs, settings):
        self.settings = settings

        classes = {}
        for name, clscfg in clscfgs.items():
            attrs = {}
            methods = {}

            for parname, par in clscfg.items():
                if parname == "Color":
                    attrs[parname] = getattr(COLOR, par.upper())
                elif parname == "Draw":
                    attrs[parname] = sum(getattr(DRAW, field.upper()) for field in par)
                elif isinstance(par, dict):
                    if "Value" in par:
                        attrs[parname] = par["Value"]
                else:
                    attrs[parname] = par

            clss = type(name, (MemoItem,), {**attrs, **methods})
            classes[name] = clss

        for name, clscfg in clscfgs.items(): # fields
            fields = {}
            for parname, par in clscfg.items():
                if isinstance(par, dict):
                    fieldtype = str
                    fieldrole = FIELD.VIEW
                    fieldusg  = USAGE.VALUE
                    for fname, fval in par.items():
                        if   fname == "Type":
                            fieldtype = fval
                            if fieldtype in classes:
                                fieldtype = classes[fieldtype]
                            else:
                                type_map = {
                                    "str": str,
                                    "int": int,
                                    "bool": bool,
                                    "float": float,
                                }
                                fieldtype = type_map.get(fieldtype.lower())
                        elif fname == "Role":
                            fieldrole = getattr(FIELD, fval.upper())
                        elif fname == "Usage":
                            fieldusg = getattr(USAGE, fval.upper())
                        if fieldusg == USAGE.LIST:
                            fieldtype = (fieldtype,)
                            
                    fields[parname] = (fieldtype, fieldrole)

            classes[name].fields = self.make_static_fields(fields)
        
        super().__init__(
            self.settings["RootPath"] + "data.xml",
            False,
            False,
            None,
            {
                'MEMO' : 
                    [clss for name, clss in classes.items()]
                ,
            }
        )

        merged_data = {}
        filenames = settings["Articles"]
        self.addSections(merged_data, filenames)
        MemoObjectModel.DATA = merged_data

    def render(self):
        draw = OM.html(name=self.settings["Articles"], engine=self.settings["Engine"], reload_time=self.settings["ReloadTime"])
        with open(self.settings["RootPath"] + self.settings["Articles"] + '.html', 'w') as file:
            file.write(draw)

def out(line):
    print("\r" + line, end="", flush=True)

with open('Classes.yaml', 'r') as file:
    classes = yaml.safe_load(file)

while True:
    out("Render...")
    try:
        with open('Memo.yaml', 'r') as file:
            settings = yaml.safe_load(file)
        
        OM = MemoObjectModel(classes, settings) # sys.argv[1]
        OM.fetch()
        OM.render()
        
    except Exception as e:
        out("Error !!!")

    if settings["RenderLoop"] <= 0:
        break

    out("Sleep ...")
    time.sleep(settings["RenderLoop"])

out("Done  ...")
