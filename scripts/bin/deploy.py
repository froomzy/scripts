

import argparse

def parse_arguments():
	parser = argparse.ArgumentParser()
	config_group = parser.add_argument_group(title='Config Files')
	parameters_group = parser.add_argument_group(
		title='Config Parameters', 
		description='These values will be ignored if a config file is provided.'
	)

	# User
	parameters_group.add_argument('-u', '--user', help='The user to login ass on the servers')
	# Ips
	parameters_group.add_argument('-i', '--ips', help='List of IPs for the servers', nargs='*')
	# Project
	parameters_group.add_argument('-p', '--project', help='The name of the project being deployed')
	# Repo
	parameters_group.add_argument('-r', '--repo', help='The url of the repo containing the code')
	# Config File
	config_group.add_argument('-c', '--config', help='The name of a config file for the deploy')

	return parser.parse_args()
	

def process_config_file(filename):
	with open(filename) as config_file:
		# This will be YAML. Load it up and turn it into a dictionary.sensible defaultsS
		pass


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