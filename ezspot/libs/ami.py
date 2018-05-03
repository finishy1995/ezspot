from aws_client import call

client = 'ec2'
ami_name = 'amzn-ami-hvm-2017.09.1.20171103-x86_64-gp2'

def get_ami_id():
    response = call(
        client,
        'describe_images',
        'Get ami info successfully.',
        Filters=[ {
          'Name': 'name',
            'Values': [
                ami_name
            ]  
        } ],
        Owners=[
            'amazon'
        ] )
    
    return response.get('Images', [{}])[0].get('ImageId', None)
