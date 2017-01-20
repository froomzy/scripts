

import argparse
import yaml
from fabric.api import execute

from ..deploy import test_task

def parse_arguments():
	parser = argparse.ArgumentParser(prog='deploy', description="Deploy a project to remote servers")
	config_group = parser.add_argument_group(title='config file')
	parameters_group = parser.add_argument_group(
		title='config parameters', 
		description='These values will be ignored if a config file is provided.'
	)
	deploy_type_group = parser.add_mutually_exclusive_group()
	
	config_group.add_argument('-c', '--config', help='The name of a config file for the deploy')

	parameters_group.add_argument('-u', '--user', help='The user to login ass on the servers')
	parameters_group.add_argument('-i', '--ips', help='List of IPs for the servers', nargs='*', metavar='IP')
	parameters_group.add_argument('-p', '--project', help='The name of the project being deployed')
	parameters_group.add_argument('-r', '--repo', help='The url of the repo containing the code')
	parameters_group.add_argument('-e', '--environemt', help='Which environment to deploy to')

	deploy_type_group.add_argument('-D', '--deploy', help='Preform an incremental deployment (default)', action='store_true')
	deploy_type_group.add_argument('-I', '--initial', help='Preform an initial deployment', action='store_true')
	deploy_type_group.add_argument('-R', '--redeploy', help='Preform a redeployment', action='store_true')
	
	return parser.parse_args()
	

def process_config_file(filename):
	with open(filename) as config_file:
		data = yaml.load(config_file)
		return data

def process_args(args):
	# Take each value from args and put into a dictionary. Sensible defaults
	pass


def main():
	args = parse_arguments()
	if args.config:
		config = process_config_file(filename=args.config)
	else:
		config = process_args(args=args)

	# TODO (Dylan): Actually do something with the config that is loaded
	execute(test_task, config=config)