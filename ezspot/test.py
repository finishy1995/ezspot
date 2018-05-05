from request import Request
from config import Config
from libs.spot_instance import start_persistent_instances
from libs.spot_instance import cancel_persistent_instances
import libs.logger as logger

class test:
    test = None

request = Request(test())
request.aws_profile = 'bjs'
request.aws_region = 'cn-northwest-1'

config = Config(request)
# start_persistent_instances(config, 1)
cancel_persistent_instances(config, 1)