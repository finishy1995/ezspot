import time
import datetime
from elastic_ip import associate_eip
from elastic_ip import disassociate_eip

def start_fleet(config, index):
    request_id = _request(config, index)
    time.sleep(5)
    
    _wait_until_completed(config.ec2Client, request_id)
    instances = _describe_fleet_instances(config.ec2Client, request_id)
    
    eip_arr = associate_eip(config.ec2Client, instances, _get_config_arr_attr(config, 'wld_fleet_tag', index))
    
    return eip_arr
    
def cancel_fleet(config, index):
    request_id = _get_fleet_request_id(config, index)
    
    if request_id != '':
        response = _cancel_fleet_request(config.ec2Client, request_id)
        
        if response.get('UnsuccessfulFleetRequests', []) == []:
            disassociate_eip(config.ec2Client, _get_config_arr_attr(config, 'wld_fleet_tag', index))
            
            return True
    
    return False

def fleet_status(config, index):
    request_id = _get_fleet_request_id(config, index)
    
    if request_id != '':
        response = _describe_fleet_instance_history(config.ec2Client, request_id)
        
        if response.get('HistoryRecords', []) != []:
            return response.get('HistoryRecords')
            
    return False

def _request(config, index):
    specification_arr = []
    specification_arr.append(_get_specification_item(config, index))
    
    response = config.ec2Client.request_spot_fleet(
        SpotFleetRequestConfig = {
            'IamFleetRole': config.wld_iam_role,
            'TargetCapacity': config.wld_instance_capacity[index],
            'TerminateInstancesWithExpiration': False,
            'LaunchSpecifications': specification_arr,
            'ReplaceUnhealthyInstances': False
        }
    )
    
    return response.get('SpotFleetRequestId')

def _get_specification_item(config, index):
    item = {
        'WeightedCapacity': 1,
    }
    params = {
        'EbsOptimized'  : 'wld_ebs_optimized',
        'ImageId'       : 'wld_instance_ami',
        'InstanceType'  : 'wld_instance_type',
        'KeyName'       : 'wld_instance_key',
        'SubnetId'      : 'wld_instance_subnet',
    }
    for key in params:
        _insert_new_key(config, params[key], index, item, key)
    
    value = _get_config_arr_attr(config, 'wld_instance_sg', index)
    if value:
        item['SecurityGroups'] = [{ 'GroupId': value }]
        
    value = _get_config_arr_attr(config, 'wld_fleet_tag', index)
    if value:
        item['TagSpecifications'] = [ {
            'ResourceType': 'instance',
            'Tags': [ {
                'Key': 'EZSpot',
                'Value': value
            } ]
        } ]
    
    return item

def _insert_new_key(config, attr, index, item, key):
    value = _get_config_arr_attr(config, attr, index)
    
    if value:
        item[key] = value

def _get_config_arr_attr(config, attr, index):
    value = getattr(config, attr, None)
    
    if value:
        return value[index]
    else:
        return None

def _wait_until_completed(client, request_id):
    for index in xrange(40):
        response = client.describe_spot_fleet_requests(
            SpotFleetRequestIds=[request_id]
        )
        
        if response.get('SpotFleetRequestConfigs')[0].get('ActivityStatus') == 'error':
            print 'Can not start spot fleet ' + request_id + ' now.'
            return False
        elif response.get('SpotFleetRequestConfigs')[0].get('ActivityStatus') == 'pending_fulfillment':
            print 'Waiting...'
            time.sleep(15)
        elif response.get('SpotFleetRequestConfigs')[0].get('ActivityStatus') == 'fulfilled':
            print 'Spot fleet ' + request_id + ' has fulfilled.'
            return True

def _describe_fleet_instances(client, request_id):
    response = client.describe_spot_fleet_instances(
        SpotFleetRequestId=request_id
    )
    
    return response.get('ActiveInstances')
    
def _get_fleet_request_id(config, index):
    response = config.ec2Client.describe_spot_fleet_requests()
    if response.get('SpotFleetRequestConfigs') != []:
        for item in response.get('SpotFleetRequestConfigs'):
            if item.get('ActivityStatus') == 'pending_fulfillment' or item.get('ActivityStatus') == 'fulfilled':
                specification = item.get('SpotFleetRequestConfig').get('LaunchSpecifications', [])
                if len(specification) == 1:
                    tags = specification[0].get('TagSpecifications', [])
                    if len(tags) == 1 and tags[0]['Tags'][0]['Key'] == 'EZSpot' and tags[0]['Tags'][0]['Value'] == config.wld_fleet_tag[index]:
                        return item.get('SpotFleetRequestId', '')
    
    return ''
    
def _cancel_fleet_request(client, request_id):
    response = client.cancel_spot_fleet_requests(
        SpotFleetRequestIds=[request_id],
        TerminateInstances=True
    )
    
    return response
    
def _describe_fleet_instance_history(client, request_id):
    print (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    
    return client.describe_spot_fleet_request_history(
        EventType='instanceChange',
        SpotFleetRequestId=request_id,
        StartTime=(datetime.datetime.now() - datetime.timedelta(days=1)),
    )
    