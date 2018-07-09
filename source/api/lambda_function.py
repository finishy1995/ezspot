from account import account_handler

def lambda_handler(event, context):
    if event['Records'][0]['eventSource'].startswith('account:'):
        return account_handler(event, context)
        
    raise Exception('Unsupported event type!')
