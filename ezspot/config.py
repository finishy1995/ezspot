import os.path
import six
from config_loader import raw_config_parse
from iam_role import get_fleet_role
from ami import get_ami_id
from libs.aws_client import client as build_client

defaultConfig = {
    'aws_profile'               : 'default',
    'prc_product_timerange'     : 168,
    'prc_product_description'   : 'Linux/UNIX (Amazon VPC)',
    'wld_fleet_number'          : 1,
    'wld_instance_type'         : ['c4.large'],
    'wld_instance_capacity'     : [1],
    'wld_fleet_tag'             : ['test'],
}

class Config:
    def __init__(self, args):
        self.ec2Client = build_client(args)
        self.iamClient = build_client(args, 'iam')
        self.lambdaClient = build_client(args, 'lambda')
        self.eventClient = build_client(args, 'events')
        self._config = defaultConfig
        
        if args.lau_config_file_path:
            config_file_path = os.path.expanduser(args.lau_config_file_path)
        else:
            config_file_path = os.path.expanduser('~/.ezspot/config')
        
        if os.path.isfile(config_file_path):
            if args.lau_config_file:
                self._config.update(raw_config_parse(config_file_path)[args.lau_config_file])
            else:
                self._config.update(raw_config_parse(config_file_path)['default'])
        
        self._config.update({k: v for k, v in six.iteritems(vars(args)) if v})
        
        if not self._config.get('wld_iam_role', None):
            self._config['wld_iam_role'] = get_fleet_role(self.iamClient)
        if not self._config.get('wld_instance_ami', None):
            ami_id = get_ami_id(self.ec2Client)
            value = []
            for index in xrange(len(self._config.get('wld_instance_type', []))):
                value.append(ami_id);
                
            self._config['wld_instance_ami'] = value

    def set_azs(self, azs):
        az_names = []
        for az in azs:
            az_names.append(az.zone_name)

        self._config['wld_instance_azs'] = az_names

    @property
    def prc_product_timerange(self):
        return self._get_required('prc_product_timerange')
        
    @property
    def prc_product_description(self):
        return self._get_required('prc_product_description')
    
    @property
    def wld_fleet_number(self):
        return self._get_required('wld_fleet_number')
    
    @property
    def wld_instance_type(self):
        return self._get_required('wld_instance_type')
        
    @property
    def wld_instance_capacity(self):
        return self._get_required('wld_instance_capacity')
        
    @property
    def wld_instance_sg(self):
        return self._get_required('wld_instance_sg')
        
    @property
    def wld_instance_ami(self):
        return self._get_required('wld_instance_ami')
        
    @property
    def wld_instance_key(self):
        return self._get_required('wld_instance_key')
        
    @property
    def wld_instance_subnet(self):
        return self._get_required('wld_instance_subnet')
        
    @property
    def wld_fleet_tag(self):
        return self._get_required('wld_fleet_tag')
        
    @property
    def wld_ebs_optimized(self):
        return self._get_required('wld_ebs_optimized')
        
    @property
    def wld_iam_role(self):
        return self._get_required('wld_iam_role')
    
    def _get_required(self, key):
        if not self._config.get(key):
            return None
        return self._config.get(key)
