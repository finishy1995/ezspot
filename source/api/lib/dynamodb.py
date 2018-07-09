import boto3

TableMap = {
    'Account': 'EZSpot-Account'
}
client = boto3.client('dynamodb', region_name='ap-northeast-1')

def list_items(**kwargs):
    '''
    List all items which meet the filters.
    
    Args:
        limit: A number how many items you want to return. Default 100.
        table: Required. A string which table you want to list
        attributes: An array which attributes you want to get in response(Will get all attributes if not set)
        filters: A list describe how to filter the result.
    '''
    
    key_condition_expression = ''
    expression_attribute_values = {}
    for filter_item in kwargs['filters']:
        key_condition_expression += filter_item['key'] + ' = :' + filter_item['key']
        expression_attribute_values[':'+filter_item['key']] = _convert_dynamodb_format(filter_item)
    
    request = {
        'Limit': kwargs['limit'] if 'limit' in kwargs else 100,
        'TableName': TableMap[kwargs['table']],
        'KeyConditionExpression': key_condition_expression,
        'ExpressionAttributeValues': expression_attribute_values,
    }
    if 'attributes' in kwargs:
        request['ProjectionExpression'] = kwargs['attributes']
    
    return _convert_normal_format_to_array(client.query(**request).get('Items', []))

def create_items(**kwargs):
    data = []
    for item in kwargs['data']:
        data.append({
            'PutRequest': {
                'Item': _convert_dynamodb_format_to_array(item)
            }
        });
    
    request = {
        'RequestItems': {
            TableMap[kwargs['table']]: data
        }
    }
    
    return client.batch_write_item(**request).get('UnprocessedItems', {})

def delete_item(**kwargs):
    request = {
        'TableName': TableMap[kwargs['table']],
        'Key': _convert_dynamodb_format_to_array(kwargs['data'])
    }
    
    if client.delete_item(**request).get('ResponseMetadata', {}).get('HTTPStatusCode', '') == 200:
        return {}
    else:
        raise Exception('Can not delete it!')

def _convert_dynamodb_format_to_array(array):
    response = {}
    for item in array:
        response[item['key']] = _convert_dynamodb_format(item)
        
    return response

def _convert_dynamodb_format(item):
    return { item['type']: str(item['value']) }
    
def _convert_normal_format_to_array(array):
    response = []
    for item in array:
        response.append(_convert_normal_format(item))
        
    return response
    
def _convert_normal_format(item):
    response = {}
    for key in item:
        value = item[key]
        if 'S' in value:
            response[key] = value['S']
        if 'N' in value:
            response[key] = int(value['N'])

    return response
