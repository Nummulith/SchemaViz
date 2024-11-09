import json

from lambda_function import lambda_handler

path = "combo"
path = "./website/data/" + path

with open(path + '_md.yaml', 'r') as file:
    metadata = file.read()

with open(path + '_dt.yaml', 'r') as file:
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

with open('./aws_lambda/lambda_test.html', 'w') as file:
    file.write(body)
