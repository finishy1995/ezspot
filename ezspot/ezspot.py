import argparse
from argparse import RawTextHelpFormatter
import sys
import workload
from version import VERSION

parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="EZSpot - the spot management tool help you to use AWS EC2 spot instance easily. ",
        epilog="Output: tab-separated variables\n\n"
              "Example:\n"
              "ezspot start \n")
parser.add_argument('--version', action='version', version=VERSION)
subparsers = parser.add_subparsers()

start_parser = subparsers.add_parser('start')
start_parser.add_argument(
    '--profile', '-p', '--aws_profile',
    help='the profile to get the AWS resources', dest="aws_profile")
start_parser.add_argument(
    '--region', '-r', '--aws_region',
    help='the region to launch the instance in', dest="aws_region")
start_parser.add_argument(
    '--access-key', '-ak', '--aws_access_key_id',
    help='the aws access key id to use', dest="aws_access_key_id")
start_parser.add_argument(
    '--secret-key', '-sk', '--aws_secret_access_key',
    help='the aws secret access key to use', dest="aws_secret_access_key")
start_parser.add_argument(
    '--config-path', '-cp', '--lau_config_file_path',
    help='the project config file path, the default is ~/.ezspot/config', dest="lau_config_file_path")
start_parser.add_argument(
    '--config', '-c', '--lau_config_file',
    help='the project config file profile type, the default is default', dest="lau_config_file")
start_parser.add_argument(
    '--fleet-number', '-n', '--wld_fleet_number',
    help='the workload fleet number. for example, if you want to start hadoop with master and slave, it should be two fleet', dest="wld_fleet_number", type=int)
start_parser.set_defaults(func=workload.start)

stop_parser = subparsers.add_parser('stop')
stop_parser.add_argument(
    '--profile', '-p', '--aws_profile',
    help='the profile to get the AWS resources', dest="aws_profile")
stop_parser.add_argument(
    '--region', '-r', '--aws_region',
    help='the region to launch the instance in', dest="aws_region")
stop_parser.add_argument(
    '--access-key', '-ak', '--aws_access_key_id',
    help='the aws access key id to use', dest="aws_access_key_id")
stop_parser.add_argument(
    '--secret-key', '-sk', '--aws_secret_access_key',
    help='the aws secret access key to use', dest="aws_secret_access_key")
stop_parser.add_argument(
    '--config-path', '-cp', '--lau_config_file_path',
    help='the project config file path, the default is ~/.ezspot/config', dest="lau_config_file_path")
stop_parser.add_argument(
    '--config', '-c', '--lau_config_file',
    help='the project config file profile type, the default is default', dest="lau_config_file")
stop_parser.set_defaults(func=workload.stop)

status_parser = subparsers.add_parser('status')
status_parser.add_argument(
    '--profile', '-p', '--aws_profile',
    help='the profile to get the AWS resources', dest="aws_profile")
status_parser.add_argument(
    '--region', '-r', '--aws_region',
    help='the region to launch the instance in', dest="aws_region")
status_parser.add_argument(
    '--access-key', '-ak', '--aws_access_key_id',
    help='the aws access key id to use', dest="aws_access_key_id")
status_parser.add_argument(
    '--secret-key', '-sk', '--aws_secret_access_key',
    help='the aws secret access key to use', dest="aws_secret_access_key")
status_parser.add_argument(
    '--config-path', '-cp', '--lau_config_file_path',
    help='the project config file path, the default is ~/.ezspot/config', dest="lau_config_file_path")
status_parser.add_argument(
    '--config', '-c', '--lau_config_file',
    help='the project config file profile type, the default is default', dest="lau_config_file")
status_parser.set_defaults(func=workload.status)

def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
