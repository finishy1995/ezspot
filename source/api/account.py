from lib.dynamodb import list_items, create_items, delete_item, update_item
import time
import random
import string

def account_handler(event):
    if event['eventSource'] == 'account':
        if event['eventMethod'] == 'GET':
            return _list(event)
        if event['eventMethod'] == 'POST':
            return _create(event)
        if event['eventMethod'] == 'DELETE':
            return _delete(event)
        if event['eventMethod'] == 'PUT':
            return _update(event)

    return { 'body': 'Unsupported event.' }
        
def _list(event):
    response = list_items(
        table='Account',
        filters=[_item(event, 'username')],
        attributes='account_id, username, account_name, ak, sk_show, account_type, create_timestamp, update_timestamp'
    )
    
    return { 'status': True, 'body': response }
    
def _create(event):
    if not 'accounts' in event['body']:
        return { 'body': 'Missing accounts information in request.' }
    
    data = []
    for index in range(len(event['body']['accounts'])):
        event['body']['accounts'][index]['account_id'] = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        data.append([
            _item(event, 'username'),
            _item(event, 'account_name', index),
            _item(event, 'ak', index),
            _item(event, 'sk', index),
            _item(event, 'sk_show', index),
            _item(event, 'account_type', index),
            _item(event, 'create_timestamp'),
            _item(event, 'update_timestamp'),
            _item(event, 'account_id')
        ])
    
    response = create_items(
        table='Account',
        data=data
    )
    if 'UnprocessedItems' in response:
        return { 'status': False, 'body': response }
    else:
        return { 'status': True, 'body': response }
    
def _update(event):
    update_list = [_item(event, 'account_name'), _item(event, 'ak'), _item(event, 'account_type'), _item(event, 'update_timestamp')]
    sk_item = _item(event, 'sk')
    if sk_item['value'] != '':
        update_list.append(sk_item)
        update_list.append(_item(event, 'sk_show'))
    
    response = update_item(
        table='Account',
        key=[_item(event, 'username'), _item(event, 'account_id')],
        updates=update_list
    )
    return { 'status': True, 'body': response }

def _delete(event):
    response = delete_item(
        table='Account',
        data=[_item(event, 'username'), _item(event, 'account_id')]
    )
    return { 'status': True, 'body': response }

def _item(event, name, index=0):
    item = {
        'key': name,
        'type': 'S',
    }
    
    if name == 'username':
        item['value'] = event['username']
    elif name == 'create_timestamp' or name == 'update_timestamp':
        item['type'] = 'N'
        item['value'] = int(time.time())
    elif name == 'sk_show':
        sk = event['body']['accounts'][index]['sk']
        item['value'] = sk[:2] + '*'*(len(sk)-4) + sk[-2:]
    elif name == 'sk':
        if not 'sk' in event['body']['accounts'][index]:
            item['value'] = ''
        else:
            item['value'] = event['body']['accounts'][index]['sk']
    else:
        item['value'] = event['body']['accounts'][index][name]
    
    return item
