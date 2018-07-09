from lib.dynamodb import list_items, create_items, delete_item

def account_handler(event):
    if event['eventSource'] == 'account':
        if event['eventMethod'] == 'GET':
            return _list(event)
    # if event['eventSource'] == 'account:POST':
    #     return _create(event['Records'][0])
    # if event['eventSource'] == 'account:PUT':
    #     return _update(event['Records'][0])
    # if event['eventSource'] == 'account:DELETE':
    #     return _delete(event['Records'][0])

    return { 'body': 'Unsupported event.' }
        
def _list(event):
    response = list_items(
        table='Account',
        filters=[_item(event, 'username')],
        attributes='account_id, username, account_name, ak, account_type, account_timestamp'
    )
    
    return { 'status': True, 'body': response }
    
def _create(event):
    data = []
    for index in range(len(event['accounts'])):
        data.append([
            _item(event, 'user_name', index),
            _item(event, 'account_name', index),
            _item(event, 'ak', index),
            _item(event, 'sk', index),
            _item(event, 'type', index),
            _item(event, 'timestamp', index),
        ])
    
    return create_items(
        table='Account',
        data=data
    )
    
def _update(event):
    if event['accounts'][0]['old_account_name'] == event['accounts'][0]['account_name']:
        return _create(event)
    else:
        _create(event)
        return delete_item(
            table='Account',
            data=[_item(event, 'user_name', 0), _item(event, 'old_account_name', 0)]
        )

def _delete(event):
    return delete_item(
        table='Account',
        data=[_item(event, 'user_name', 0), _item(event, 'account_name', 0)]
    )

def _item(event, name, index=0):
    item = {
        'key': name,
        'type': 'S',
    }
    
    if name == 'username':
        item['value'] = event['username']
    # else:
    #     item['value'] = event['accounts'][index][name]
        
    if name == 'timestamp':
        item['type'] = 'N'
    
    return item
