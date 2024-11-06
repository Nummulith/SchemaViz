import os
import json
import yaml
import inspect

import subprocess

from ObjectModelFramework import SchemaVizObjectModel

class lambda_invoke:
    def response(body, status_code=200, as_html=False):
        res = {
            'statusCode': status_code,
            'body': (body if type(body) == str else json.dumps(body))
        }

        if as_html:
            res['headers'] = {
                'Content-Type': 'text/html'
            }
        else:
            res['headers'] = {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }

        return res

    @staticmethod
    def root_get_handler(event, context):
        html_list = '<ul>'
        for name in lambda_invoke.get_static_methods():
            core, tail = tuple(name.rsplit('_', 1)) if '_' in name else (name, "")
            if core == "" or core == "lambda" or core == "invalidpath" or tail != "handler":
                continue
            resource, method = tuple(core.rsplit('_', 1)) if '_' in core else (core, "")
            if resource == "root" or (method != "get" and method != "post"):
                continue
            html_list += f'<li><a href="/{resource}">{resource}.{method}</a></li>'
        html_list += '</ul>'
        return lambda_invoke.response(html_list, 200, True)

    @staticmethod
    def invalidpath_handler(event, context):
        return lambda_invoke.response(f"Invalid query:\nPath: {event['path']}\nMethod: {event['httpMethod']}")

    @classmethod
    def get_functions():
        return {key: value for key, value in inspect.getmembers(__import__(__name__)) if inspect.isfunction(value)}

    @classmethod
    def get_static_methods(cls):
        types = {}
        for curcls in inspect.getmro(cls):
            for dict_name, dict_item in curcls.__dict__.items():
                if dict_name[:2] == "__":
                    continue
                types[dict_name] = dict_item
        
        members = inspect.getmembers(cls, predicate=inspect.isfunction)
        static_methods = {name: func for name, func in members if type(types[name]) == staticmethod}
        return static_methods

    @classmethod
    def lambda_handler(cls, event, context):
        if "path" not in event:
            return lambda_invoke.response(event, 400)

        func = event['path'][1:]
        func = func.replace('/', '_')
        func = "root" if func == "" else func
        func += "_"
        func += event['httpMethod'].lower() + "_"
        func += "handler"

        functions = cls.get_static_methods()
        handler = functions[func] if func in functions else cls.invalidpath_handler

        return handler(event, context)

class lambda_viz(lambda_invoke):
    @staticmethod
    def viz_post_handler(event, context):
        body = event["body"]
        body = json.loads(body)

        OM = SchemaVizObjectModel(yaml.safe_load(body["metadata"]), yaml.safe_load(body["data"]))
        OM.fetch()
        draw = OM.html(None, "", "dot", 0, html_wrap=False)

        res = {
            'result': draw,
        }

        print(draw)

        return lambda_invoke.response(res)

def print_directory_structure(path, indent=0):
    if indent > 5:
        return ""

    structure = ""
    try:
        for item in os.listdir(path):
            if item is None:
                continue

            item_path = os.path.join(path, item)

            if item == "dot_builtins":
                structure += path + "/" + item + '\n' # ('+' * indent) + 

            if os.path.isdir(item_path):
                structure += print_directory_structure(item_path, indent + 1)

    except PermissionError:
        # structure += ('*' * indent) + 'Permission denied: ' + path + '\n'
        pass

    except Exception as e:
        # structure += ('*' * indent) + 'Error accessing: ' + str(e) + '\n'
        pass
    
    return structure

def call_bash(cmnd):
    try:
        print("Command: ", cmnd)

        result = subprocess.run(cmnd, capture_output=True, text=True, env={"PATH": os.environ["PATH"] + ":/opt/python/bin"})
        
        print("Command output:", result.stdout)
        print("Command error:", result.stderr)
    except Exception as e:
        print(f"Error executing command: {e}")

def lambda_handler(event, context):
    # directory_to_print = '/'
    # print(f"ls {directory_to_print}:")
    # print(print_directory_structure(directory_to_print))

    os.environ["PATH"] += os.pathsep + '/opt/python/bin'

    # call_bash(["ls", "-l", "/lib64"])

    # echo 'digraph G { A -> B; B -> C; C -> A; }' > test.dot
    call_bash(["echo", "'digraph G { A -> B; B -> C; C -> A; }'", ">", "test.dot"])

    # dot -Tpng test.dot -o test_output.png
    call_bash(["/opt/python/bin/dot", "-Tpng", "test.dot", "-o", "test_output.png"])

    return lambda_viz.lambda_handler(event, context)
