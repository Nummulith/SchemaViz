# Custom Handlers

class lambda_hello_world(lambda_invoke):
    @staticmethod
    def hello_get_handler(event, context):
        return lambda_invoke.response('Hello World!')

    @staticmethod
    def event_get_handler(event, context):
        return lambda_invoke.response(event)
        
    @staticmethod
    def context_get_handler(event, context):
        return lambda_invoke.response(str(context))
        
    @staticmethod
    def array_get_handler(event, context):
        return lambda_invoke.response(["theese", "are", "many", "strin"])

class lambda_books(lambda_invoke):
    @staticmethod
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
                    return lambda_invoke.response(book)
        return lambda_invoke.response(f'Book with id {id} not found', 404)

        return lambda_invoke.response(db)

class lambda_db(lambda_invoke):
    @staticmethod
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
        
        return lambda_invoke.response("inserted successfully!")

    @staticmethod
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
            return lambda_invoke.response(item)
        else:
            return lambda_invoke.response('Item not found', 404)

