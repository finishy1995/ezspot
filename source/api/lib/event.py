import boto3
import json

client = boto3.client('cognito-idp')

def generate_event(event):
    new_event = {}
    new_event['eventSource'] = event['path'][1:] if 'path' in event else ''
    new_event['eventMethod'] = event['httpMethod'] if 'httpMethod' in event else ''
    new_event['username'] = _get_user_name(event)
    new_event['body'] = json.loads(event['queryStringParameters']['body']) if 'body' in event['queryStringParameters'] else {}
    
    return new_event

def _get_user_name(event):
    response = client.get_user(AccessToken=event['queryStringParameters']['accessT'])
    return response['Username']
