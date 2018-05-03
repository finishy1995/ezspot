import os.path
import six
from config_loader import raw_config_parse
import libs.logger as logger
from libs.iam_role import get_fleet_role
from libs.ami import get_ami_id
from libs.aws_client import client as build_client
from libs.aws_client import error_handler

class Config:
    def __init__(self, args, flag=False):
        build_client(args)
        build_client(args, 'iam')
        self._config = self.default_config(args.wld_fleet_number)
        
        if args.lau_config_file_path:
            config_file_path = os.path.expanduser(args.lau_config_file_path)
        else:
            config_file_path = os.path.expanduser('~/.ezspot/config')
        
        if os.path.isfile(config_file_path):
            if args.lau_config_file:
                self._config.update(raw_config_parse(config_file_path)[args.lau_config_file])
                logger.debug('Config load custom setting field - ' + args.lau_config_file)
            else:
                self._config.update(raw_config_parse(config_file_path)['default'])
                logger.debug('Config load custom setting field - default')
            logger.debug('Config load custom setting in file ' + config_file_path + ' successfully.')
        else:
            logger.debug('Not find custom setting in file ' + config_file_path + '.')
        
        self._config.update({k: v for k, v in six.iteritems(vars(args)) if v})
        
        fleet_number = self._config.get('wld_fleet_number', None)
        if fleet_number:
            self._config['wld_fleet_number'] = int(fleet_number)
        capacity = self._config.get('wld_instance_capacity', None)
        if capacity:
            for index in xrange(len(capacity)):
                capacity[index] = int(capacity[index])
        logger.info('Config load successfully.')
        
        if flag:
            if not self._config.get('wld_iam_role', None):
                logger.warning('Not find wld_iam_role in your config. Trying to get a role from your AWS account.')
                role = get_fleet_role()
                if role:
                    self._config['wld_iam_role'] = role
                    logger.info('Find AWS default service role in your AWS account. Use it as default spot fleet role.')
                else:
                    error_handler(
                        'Can not find a valid iam role for spot fleet in your AWS account. Please open your console to create one first!',
                        'Failed to run method: Config.'
                    )
            
            if not self._config.get('wld_instance_ami', None):
                logger.warning('Not find wld_instance_ami in your config. Trying to get a ami from your AWS account.')
                ami_id = get_ami_id()
                if ami_id:
                    value = []
                    for index in xrange(self._config.get('wld_fleet_number', 1)):
                        value.append(ami_id);
                    self._config['wld_instance_ami'] = value
                    logger.info('Find AWS default instance ami in your AWS account. Use it as default spot fleet ami.')
                else:
                    error_handler(
                        'Can not find a valid ami id for spot fleet in your AWS account. Please set it in config wld_instance_ami.',
                        'Failed to run method: Config.'
                    )

    def default_config(self, number):
        if not number:
            number = 1
            
        config = {
            'aws_profile'               : 'default',
            'prc_product_timerange'     : 168,
            'prc_product_description'   : 'Linux/UNIX (Amazon VPC)',
            'wld_fleet_number'          : number,
            'wld_instance_type'         : [],
            'wld_instance_capacity'     : [],
            'wld_fleet_tag'             : [],
        }
        
        for index in xrange(number):
            config['wld_instance_type'].append('c4.large')
            config['wld_instance_capacity'].append(1)
            config['wld_fleet_tag'].append('test' + str(number))
        
        logger.debug('Config load default setting successfully.')
        return config

    def set_azs(self, azs):
        az_names = []
        for az in azs:
            az_names.append(az.zone_name)

        self._config['wld_instance_azs'] = az_names
        
    def set_subnet(self, subnet, index):
        if self._config.get('wld_instance_subnet', None) == None:
            self._config['wld_instance_subnet'] = []
            for index in xrange(self._config['wld_fleet_number']):
                self._config['wld_instance_subnet'].append('')
        
        self._config['wld_instance_subnet'][index] = subnet

    def __getattr__(self, key):
        if not self._config.get(key):
            return None
        return self._config.get(key)
