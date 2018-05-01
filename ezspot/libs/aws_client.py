import boto3
import botocore
from functools import partial

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
        return client(
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key)
    else:
        return client()
