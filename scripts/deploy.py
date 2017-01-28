from fabric.api import *
from fabric.network import disconnect_all
import petname
from contextlib import contextmanager as _contextmanager
from collections import namedtuple


root_deploy_dir = '~/deployments'
deployment_dir = ''


DeploymentStatus = namedtuple('DeploymentStatus')

@_contextmanager
def virtualenv():
	with cd(env.env_directory):
		with prefix(env.env_activate):	
			yield		


def set_hosts(user, hosts):
	return ['{user}@{ip}'.format(user=user, ip=ip) for ip in hosts]


def get_user():
	return input('Enter host user: ')


def get_hosts():
	hosts = []
	while True:
		host = input('Enter host IP (f to finish): ')
		if host.upper() == 'F':
			break
		else:
			hosts.append(host)
	return hosts


def set_role_defs(user, hosts):
	role_defs = {
		'root': set_hosts('root', hosts),
		'www': set_hosts(user, hosts)
	}
	env.roledefs = role_defs


def make_deployment_dir(deployment_dir):
	run('mkdir -p {dir}'.format(dir=deployment_dir))


def clone_repository(repository, deployment_dir):
	with cd(deployment_dir):
		run('git clone {} .'.format(repository), pty=False)


def pull_repository(repository, deployment_dir):
	with cd(deployment_dir):
		run('git clone {} .'.format(repository), pty=False)


def get_existing_directory(project):
	project_dir = '{root}/{project}'.format(root=root_deploy_dir, project=project)
	with cd(project_dir):
		return run("ls -td -- */ | head -n 1 ")


def print_status(status):
	pass
	

def deploy(config, hosts):
	try:
		dir = execute(get_existing_directory, project=config['name'], hosts=hosts['user_hosts'])
		deployment_dir = '{root}/{project}/{dir}'.format(
			root=root_deploy_dir, 
			project=config['name'], 
			dir=dir
		)
		print('Beginning a new deployment...')
		print('Step One: Create a new folder to deploy into...')
		execute(make_deployment_dir, deployment_dir, hosts=hosts['user_hosts'])
		print('Step One: Complete...')
		execute(clone_repository, config['repo'], deployment_dir, hosts=hosts['user_hosts'])
		print('Step Two: Clone project into new folder...')

		print('Step Two: Complete...')

		print('Step Three: Update virtualenv...')

		print('Step Three: Complete...')

		print('Step Four: Create symbolic link...')

		print('Step Four: Complete...')

		print('Step Five: Graceful reload of nginx...')

		print('Step Five: Complete...')

		print('Deployment completed...')
	finally:
		disconnect_all()


def ll():
	run('ls')

def test_task(config, hosts):
	try:
		print('Hello World')
		execute(get_existing_directory, config['name'], hosts=hosts['user_hosts'])
	finally:
		disconnect_all()



# @task
# def initial_deployment(repository, project_name):
# 	# Create server block
# 	# Create Site Available (?? if I have to)
# 	# Run a new deployment
# 	pass