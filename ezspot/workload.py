from config import Config
from request import Request
from libs.spot_fleet import start_fleet
from libs.spot_fleet import cancel_fleet
from libs.spot_fleet import fleet_status
import libs.logger as logger

def start(args):
    config = Config(Request(args), True)
    for index in xrange(config.wld_fleet_number):
        start_fleet(config, index)
    
    logger.info('Workload start successfully. Enjoy!')

def stop(args):
    config = Config(Request(args))
    for index in xrange(config.wld_fleet_number):
        cancel_fleet(config, index)
    
    logger.info('Workload stop successfully.')
    
def status(args):
    # config = Config(Request(args))
    # for index in xrange(config.wld_fleet_number):
    #     fleet_status(config, index)
    
    print "Status are not supported right now."
