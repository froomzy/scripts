from fabric.api import *
import petname
from contextlib import contextmanager as _contextmanager

root_deploy_dir = '~/deployments'
deployment_dir = ''

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


def set_role_defs(user):
	hosts = get_hosts()
	role_defs = {
		'root': set_hosts('root', hosts),
		'www': set_hosts(user, hosts)
	}
	env.roledefs = role_defs

@roles('www')
def make_deployment_dir(deployment_dir):
	run('mkdir -p {dir}'.format(dir=deployment_dir))


@roles('www')
def clone_repository(repository, deployment_dir):
	with cd(deployment_dir):
		run('git clone {} .'.format(repository), pty=False)


@task
def deploy(project, repository):
	user = get_user()
	deployment_dir = '{root}/{project}/{dir}'.format(root=root_deploy_dir, project=project, dir=petname.Generate(words=3, separator='-'))
	set_role_defs(user=user)
	print('Beginning a new deployment...')
	print('Step One: Create a new folder to deploy into...')
	execute(make_deployment_dir, deployment_dir)
	print('Step One: Complete...')
	execute(clone_repository, repository, deployment_dir)
	print('Step Two: Clone project into new folder...')

	print('Step Two: Complete...')

	print('Step Three: Update virtualenv...')

	print('Step Three: Complete...')

	print('Step Four: Create symbolic link...')

	print('Step Four: Complete...')

	print('Step Five: Graceful reload of nginx...')

	print('Step Five: Complete...')

	print('Deployment completed...')



# @task
# def initial_deployment(repository, project_name):
# 	# Create server block
# 	# Create Site Available (?? if I have to)
# 	# Run a new deployment
# 	pass