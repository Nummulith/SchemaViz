import json
import inspect
import boto3

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

def get_functions():
    return {key: value for key, value in inspect.getmembers(__import__(__name__)) if inspect.isfunction(value)}


# Custom Handlers

def hello_get_handler(event, context):
    return response('Hello World!')

def event_get_handler(event, context):
    return response(event)
    
def context_get_handler(event, context):
    return response(str(context))
    
def array_get_handler(event, context):
    return response(["theese", "are", "many", "strin"])
    
def books_get_handler(event, context):
    db = [
        {
            "id": 1,
            "title": "Becoming",
            "author": "Michelle Obama",
            "price": 22.99 
        },
        {
            "id": 2,
            "title": "Humans of New York",
            "author": "Brandon Stanton",
            "price": 19.99 
        }  
    ]

    try:
      id = int(event['queryStringParameters']['id'])
    except:
      id = 0
      
    if (id > 0):
      for book in db:
        if book["id"] == id:
          return response(book)
      return response(f'Book with id {id} not found', 404)

    return response(db)


# db

def db_ins_get_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = "key-door-soul-players-data"
    table = dynamodb.Table(table_name)
    
    item = {
        'PlayerID': "Player0001",
        'GameID': "Game0001",
        'Score': "351"
    }
    
    table.put_item(Item=item)
    
    return response("inserted successfully!")

def db_read_get_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = "key-door-soul-players-data"
    table = dynamodb.Table(table_name)
    
    resp = table.get_item(
        Key={
            'PlayerID': "Player0001",
            'GameID': "Game0001",
        }
    )
    item = resp.get('Item')
    
    if item:
        return response(item)
    else:
        return response('Item not found', 404)


# Viz

def viz_post_handler(event, context):
    print("event: "  , event)
    print("context: ", vars(context))

    res = {
        'context': str(vars(context)),
        'event':   str(event),
        'body':   str(event["body"]),
    }

    return response(res)


# Default handlers

def invalidpath_handler(event, context):
    return response(f"Invalid query:\nPath: {event['path']}\nMethod: {event['httpMethod']}")

def root_get_handler(event, context):
    html_list = '<ul>'
    for name in get_functions():
        core, tail = tuple(name.rsplit('_', 1)) if '_' in name else (name, "")
        if core == "" or core == "lambda" or core == "invalidpath" or tail != "handler":
           continue
        resource, method = tuple(core.rsplit('_', 1)) if '_' in core else (core, "")
        if resource == "root" or (method != "get" and method != "post"):
           continue
        html_list += f'<li><a href="/{resource}">{resource}.{method}</a></li>'
    html_list += '</ul>'
    return response(html_list, 200, True)

class lambda_invoke:
    @classmethod
    def get_static_methods(cls):
        # Получить все члены класса, которые являются функциями
        members = inspect.getmembers(cls, predicate=inspect.isfunction)
        
        # Фильтровать только статические методы
        static_methods = {name: func for name, func in members if isinstance(getattr(cls, name), staticmethod)}
        
        return static_methods

    @staticmethod
    def lambda_handler(event, context):
        if "path" not in event:
            return response(event, 400)

        func = event['path'][1:]
        func = func.replace('/', '_')
        func = "root" if func == "" else func
        func += "_"
        func += event['httpMethod'].lower() + "_"
        func += "handler"

        print(func)

        functions = get_functions()
        handler = functions[func] if func in functions else invalidpath_handler

        return handler(event, context)

def lambda_handler(event, context):
    if "path" not in event:
       return response(event, 400)

    func = event['path'][1:]
    func = func.replace('/', '_')
    func = "root" if func == "" else func
    func += "_"
    func += event['httpMethod'].lower() + "_"
    func += "handler"

    print(func)

    functions = get_functions()
    handler = functions[func] if func in functions else invalidpath_handler

    return handler(event, context)
