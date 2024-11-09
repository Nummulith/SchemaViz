import os
import json
import yaml
import inspect

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

        try:
            res = handler(event, context)
        except Exception as e:
            res = lambda_invoke.response(f"Internal Server Lambda_Viz Error: {e}", 500)

        return res

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

        return lambda_invoke.response(res)

def lambda_handler(event, context):
    os.environ['PATH'] = '/opt/python/bin:' + os.environ['PATH']

    return lambda_viz.lambda_handler(event, context)

# https://lifeinplaintextblog.wordpress.com/deploying-graphviz-on-aws-lambda/
