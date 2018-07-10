from account import account_handler
from lib.event import generate_event
import json

def lambda_handler(event, context):
    print(event)
    event = generate_event(event)
    
    if not 'eventSource' in event or not 'username' in event:
        response = { 'body': 'Unsupported API call.' }
    elif event['eventSource'].startswith('account'):
        response = account_handler(event)
    else:
        response = { 'body': 'Unsupported event.' }
        
    result = {
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'statusCode': 500
    }
    if 'status' in response and response['status'] == True:
        result['statusCode'] = 200
    if 'body' in response:
        result['body'] = json.dumps(response['body'])
        
    return result
