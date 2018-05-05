from config import Config
from request import Request
from libs.spot_fleet import start_fleet
from libs.spot_fleet import cancel_fleet
from libs.spot_fleet import fleet_status
from libs.spot_instance import start_persistent_instances
from libs.spot_instance import cancel_persistent_instances
from libs.instance import start_on_demand_instances
from libs.instance import cancel_on_demand_instances
from libs.resources import clean as resources_clean
import libs.logger as logger

def start(args):
    if args.debug:
        logger.setLevel(args.debug)
    
    config = Config(Request(args), True)
    for index in xrange(config.wld_fleet_number):
        if config.wld_fleet_type == 'persistent':
            start_persistent_instances(config, index)
        elif config.wld_fleet_type == 'on-demand':
            start_on_demand_instances(config, index)
        else:
            start_fleet(config, index)
    
    logger.info('Workload start successfully. Enjoy!')

def stop(args):
    if args.debug:
        logger.setLevel(args.debug)
    
    config = Config(Request(args))
    for index in xrange(config.wld_fleet_number):
        if config.wld_fleet_type == 'persistent':
            cancel_persistent_instances(config, index)
        elif config.wld_fleet_type == 'on-demand':
            cancel_on_demand_instances(config, index)
        else:
            cancel_fleet(config, index)
    
    logger.info('Workload stop successfully.')
    
def status(args):
    if args.debug:
        logger.setLevel(args.debug)
    
    config = Config(Request(args))
    total_price = 0.0
    for index in xrange(config.wld_fleet_number):
        if config.wld_fleet_type == 'persistent':
            continue
        elif config.wld_fleet_type == 'on-demand':
            continue
        else:
            price = fleet_status(config, index)
            if price:
                total_price += price

    if config.wld_fleet_type == 'persistent':
        logger.info('We dont support persistent status yet.')
    elif config.wld_fleet_type == 'on-demand':
        logger.info('We dont support on-demand status yet.')
    else:
        logger.info('Workload total price : ' + str(total_price))
        logger.info("Workload status all show.")

def clean(args):
    if args.debug:
        logger.setLevel(args.debug)
    
    config = Config(Request(args))
    resources_clean()
