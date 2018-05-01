from config import Config
from request import Request
from spot_fleet import start_fleet
from spot_fleet import cancel_fleet
from spot_fleet import fleet_status

def start(args):
    config = Config(Request(args))
    for index in xrange(config.wld_fleet_number):
        start_fleet(config, index)

def stop(args):
    config = Config(Request(args))
    for index in xrange(config.wld_fleet_number):
        cancel_fleet(config, index)
    
def status(args):
    # config = Config(Request(args))
    # for index in xrange(config.wld_fleet_number):
    #     fleet_status(config, index)
    
    print "Status are not supported right now."
