import boto3
import zipfile
import os
import time
from iam_role import create_eip_handler_role

def create_eip_handler(config, index, eip_arr):
    name = 'EZSpot-' + config.wld_fleet_tag[index] + '-eip-handler'
    role = create_eip_handler_role(config.iamClient, name)
    time.sleep(5)
    file = _create_eip_handler_zipfile()
    
    _create_lambda(
        config.lambdaClient,
        name,
        role,
        { 'ZipFile': open(file, 'rb').read() },
        'eip_handler.lambda_handler',
        180,
        256
    )
    
    os.remove(file)

# AWS BJS not support environment variables
def _create_lambda(client, name, role, code, handler, timeout=3, memorySize=128):
    client.create_function(
        FunctionName=name,
        Runtime='python2.7',
        Role=role,
        Handler=handler,
        Code=code,
        Timeout=timeout,
        MemorySize=memorySize
    )

def _create_eip_handler_zipfile():
    f = zipfile.ZipFile('eip_handler_zipfile.zip', 'w', zipfile.ZIP_DEFLATED)
    f.write('elastic_ip.py')
    f.write('eip_handler.py')
    f.close()
    
    return 'eip_handler_zipfile.zip'
    