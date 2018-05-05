import boto3
import botocore
import logger
from functools import partial

class Resource:
    clients = {}
    destroy = []
    
    def destroy_back(self):
        for index in xrange(len(self.destroy) - 1, -1, -1):
            self.destroy[index][0](self.destroy[index][1])
            
        logger.info('All AWS resources which have been created in this project has been rollback.')
resources = Resource()

def client(args, service='ec2'):
    if args.aws_profile:
        boto3.setup_default_session(profile_name=args.aws_profile)

    client = partial(boto3.client, service)
        
    if args.aws_region:
        # TODO: Add profile support BJS Lambda
        if (service == 'lambda' or service == 'events') and args.aws_region == 'cn-northwest-1':
            client = partial(client, 'cn-north-1')
        else:
            client = partial(client, args.aws_region)
        
    if args.aws_access_key_id and args.aws_secret_access_key:
        resources.clients[service] = client(
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key)
    else:
        resources.clients[service] =  client()

def call(client, method, message=None, runback=None, **kwargs):
    _debug_output(client, method, **kwargs)
    func = getattr(resources.clients[client], method)
    try:
        response = func(**kwargs)
    except Exception, args:
        error_handler(str(args), "Failed to run client : {0}, method: {1}".format(client, method))
    else:
        if message:
            logger.debug(message)
            
        if runback:
            resources.destroy.append([runback, response])
            
        return response

def error_handler(log_message, runtime_message):
    logger.error(log_message)
    resources.destroy_back()
    raise RuntimeError(runtime_message)
    
def get_waiter(client, waiter_type):
    func = getattr(resources.clients[client], 'get_waiter')
    
    if func:
        return func(waiter_type)
    else:
        error_handler('Can not wait for the client.', "Failed to create a wait client for {0}.".format(waiter_type))

def _debug_output(client, method, **kwargs):
    words = "Trying to run client: {0}, method: {1} .".format(client, method)
    if len(kwargs) > 0:
        words += " Args are as following: "
    
    logger.debug(words)
    for key in kwargs:
        logger.debug('    ' + key + ' = ' + str(kwargs[key]))
