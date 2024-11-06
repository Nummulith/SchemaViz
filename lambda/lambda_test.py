import json

from lambda_function import lambda_handler

with open('./website/metadata.yaml', 'r') as file:
    metadata = file.read()

with open('./website/data.yaml', 'r') as file:
    data = file.read()

param = {
    "metadata": metadata,
    "data": data,
};

res = lambda_handler({
        'httpMethod': "Post",
        "path": '/viz',
        "body": json.dumps(param),
    }, {}
)

body = res["body"]
body = json.loads(body)
body = body["result"]

with open('./lambda/lambda_test.html', 'w') as file:
    file.write(body)
