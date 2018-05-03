from request import Request
from config import Config
from libs.spot_fleet import start_fleet
from libs.spot_fleet import cancel_fleet
import libs.logger as logger

class test:
    test = None

request = Request(test())
request.aws_profile = 'bjs'
request.aws_region = 'cn-northwest-1'

config = Config(request)
# print config.wld_iam_role
# start_fleet(config, 0)
cancel_fleet(config, 0)
