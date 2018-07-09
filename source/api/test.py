from lambda_function import lambda_handler

test_event_list = {
    'path': '/account',
    'httpMethod': 'GET',
    'queryStringParameters': {
    }
}

print(lambda_handler(test_event_list, ''))
