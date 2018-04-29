from request import Request
from config import Config
from price import get_az_arr
from spot_fleet import start_fleet
from spot_fleet import cancel_fleet
from spot_fleet import fleet_status
from libs.aws_client import client as build_client

request = Request()
request.aws_profile = 'bjs'
request.aws_region = 'cn-northwest-1'

ec2Client = build_client(request)
iamClient = build_client(request, 'iam')
config = Config([ec2Client, iamClient], request)

# config.set_azs(get_az_arr(config))

# print start_fleet(config, 0)
# print cancel_fleet(config, 0)
# print fleet_status(config, 0)
