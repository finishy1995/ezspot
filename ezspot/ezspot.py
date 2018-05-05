import argparse
from argparse import RawTextHelpFormatter
import sys
import workload
from version import VERSION

parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="EZSpot - the spot management tool help you to use AWS EC2 spot instance easily. ",
        epilog="Output: INFO & WARNING & ERROR as text format.\n\n"
              "Example:\n"
              "ezspot start \n")
parser.add_argument('--version', action='version', version=VERSION)
subparsers = parser.add_subparsers()

start_parser = subparsers.add_parser('start')
start_parser.set_defaults(func=workload.start)
stop_parser = subparsers.add_parser('stop')
stop_parser.set_defaults(func=workload.stop)
status_parser = subparsers.add_parser('status')
status_parser.set_defaults(func=workload.status)
clean_parser = subparsers.add_parser('clean')
clean_parser.set_defaults(func=workload.clean)

def add(*args, **kwargs):
    start_parser.add_argument(*args, **kwargs)
    stop_parser.add_argument(*args, **kwargs)
    status_parser.add_argument(*args, **kwargs)
    clean_parser.add_argument(*args, **kwargs)
    
add('--profile', '-p', '--aws_profile',
    help='the profile to get the AWS resources', dest="aws_profile")
add('--region', '-r', '--aws_region',
    help='the region to launch the instance in', dest="aws_region")
add('--access-key', '-ak', '--aws_access_key_id',
    help='the aws access key id to use', dest="aws_access_key_id")
add('--secret-key', '-sk', '--aws_secret_access_key',
    help='the aws secret access key to use', dest="aws_secret_access_key")
add('--config-path', '-cp', '--lau_config_file_path',
    help='the project config file path, the default is ~/.ezspot/config', dest="lau_config_file_path")
add('--config', '-c', '--lau_config_file',
    help='the project config file profile type, the default is default', dest="lau_config_file")
add('--fleet-number', '-n', '--wld_fleet_number',
    help='the workload fleet number. for example, if you want to start hadoop with master and slave, it should be 2 fleet', dest="wld_fleet_number", type=int)
add('--fleet-type', '-t', '--wld_fleet_type',
    help='the workload fleet type.', dest="wld_fleet_type", type=str, choices=['normal', 'persistent', 'on-demand'])
add('--block-duration', '-bd', '--wld_block_duration',
    help='the workload fleet block duration, only work at type \'persistent\'.', dest="wld_block_duration", nargs='*')
add('--instance-type', '-it', '--wld_instance_type',
    help='the workload instance type.', dest="wld_instance_type", nargs='*')
add('--instance-azs', '-azs', '--wld_instance_azs',
    help='the workload instance az.', dest="wld_instance_azs", nargs='*')
add('--instance-capacity', '-capacity', '--wld_instance_capacity',
    help='the workload instance capacity.', dest="wld_instance_capacity", nargs='*')
add('--instance-sg', '-sg', '--wld_instance_sg',
    help='the workload instance security group.', dest="wld_instance_sg", nargs='*')
add('--instance-ami', '-image', '--wld_instance_ami',
    help='the workload instance ami id.', dest="wld_instance_ami", nargs='*')
add('--instance-key', '-key', '--wld_instance_key',
    help='the workload instance ssh key.', dest="wld_instance_key", nargs='*')
add('--instance-subnet', '-subnet', '--wld_instance_subnet',
    help='the workload instance subnet.', dest="wld_instance_subnet", nargs='*')
add('--wld-tag', '-tag', '--wld_fleet_tag',
    help='the workload tag, it should be unique in your projects.', dest="wld_fleet_tag", nargs='*')
add('--ebs-optimized', '-ebs', '--wld_ebs_optimized',
    help='the workload instance ebs optimized.', dest="wld_ebs_optimized", nargs='*')
add('--iam-role', '-role', '--wld_iam_role',
    help='the workload iam role.', dest="wld_iam_role", nargs='*')
add('--product-description', '-product', '--prc_product_description',
    help='the workload instance product description.', dest="prc_product_description", nargs='*')
add('--product-timerange', '--prc_product_timerange',
    help='the workload instance product timerange.', dest="prc_product_timerange", nargs='*')
add('--debug',
    help='the debug information level.', dest="debug", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])

def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
