

import argparse
import yaml
from fabric.api import execute

from ..deploy import test_task, deploy
import version

def parse_arguments():
	parser = argparse.ArgumentParser(prog='deploy', description="Deploy a project to remote servers")
	config_group = parser.add_argument_group(title='config file')
	parameters_group = parser.add_argument_group(
		title='config parameters', 
		description='These values will be ignored if a config file is provided.'
	)
	deploy_type_group = parser.add_mutually_exclusive_group()
	parser.add_argument('-v', '--version', help='Version details', action='store_true')
	parser.add_argument('-e', '--environment', help='Which environment to deploy to')
	
	config_group.add_argument('-c', '--config', help='The name of a config file for the deploy')

	parameters_group.add_argument('-u', '--user', help='The user to login ass on the servers')
	parameters_group.add_argument('-i', '--ips', help='List of IPs for the servers', nargs='*', metavar='IP')
	parameters_group.add_argument('-p', '--project', help='The name of the project being deployed')
	parameters_group.add_argument('-r', '--repo', help='The url of the repo containing the code')

	deploy_type_group.add_argument('-D', '--deploy', help='Preform an incremental deployment (default)', action='store_true')
	deploy_type_group.add_argument('-I', '--initial', help='Preform an initial deployment', action='store_true')
	deploy_type_group.add_argument('-R', '--redeploy', help='Preform a redeployment', action='store_true')
	
	return parser.parse_args()
	

def process_config_file(filename, environment):
	with open(filename) as config_file:
		data = yaml.load(config_file)
	print(data)
	config = data['environments'][environment]
	config.update(data['project'])
	return config

def process_args(args):
	# Take each value from args and put into a dictionary. Sensible defaults
	pass


def print_version_details():
	print('Deploy scripts version {version}'.format(version=version.__version__))


def set_hosts(user, hosts):
	return ['{user}@{ip}'.format(user=user, ip=ip) for ip in hosts]


def set_role_defs(user, hosts):
	role_defs = {
		'root': set_hosts('root', hosts),
		'www': set_hosts(user, hosts)
	}
	env.roledefs = role_defs


def main():
	args = parse_arguments()
	if args.version:
		print_version_details()
		return
	if args.config:
		config = process_config_file(filename=args.config, environment=args.environment)
	else:
		config = process_args(args=args)
	hosts = {
		'user_hosts': set_hosts(user=config['user'], hosts=config['hosts']),
		'root_hosts': set_hosts(user='root', hosts=config['hosts']),
	}
	# TODO (Dylan): Actually do something with the config that is loaded
	deploy(config=config, hosts=hosts)