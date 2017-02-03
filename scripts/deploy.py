from fabric.api import *
from fabric.network import disconnect_all
import petname
from contextlib import contextmanager as _contextmanager
from collections import namedtuple


root_deploy_dir = '~/deployments'
root_site_dir = '~/sites'
root_log_dir = '~/logs'
deployment_dir = ''


InitialDeploymentStatus = namedtuple(
	'InitialDeploymentStatus',
	field_names=[
		'create_directories',
		'clone_code',
		'create_venv',
		'migrate',
		'static',
		'config_gunicorn',
		'config_nginx',
		'reload'
	]
)


DeploymentStatus = namedtuple(
	'DeploymentStatus', 
	field_names=[
		'pull_code',
		'update_venv',
		'migrate',
		'static',
		'reload'
	]
)


ReDeploymentStatus = namedtuple(
	'ReDeploymentStatus',
	field_names=[
		'create_directory',
		'clone_code',
		'create_venv',
		'migrate',
		'static',
		'config_nginx'
		'reload',
		'clear_old'
	]
)


@_contextmanager
def virtualenv(directory):
	activate = 'source {dir}/.venv/bin/activate'.format(dir=directory)
	with prefix(activate):
		yield		


def create_directories(deployment_dir, site_dir):
	run('mkdir -p {dir}'.format(dir=deployment_dir))
	run('mkdir -p {dir}'.format(dir=site_dir))
	run('mkdir -p {dir}'.format(dir=log_dir))

def create_virtualenv(deployment_dir):
	with cd(deployment_dir):
		run('virtualenv -p python3 env')
		with virtualenv(deployment_dir):
			run('pip install -r requirements.txt')


def migrate_database(deployment_dir, environment):
	with cd(deployment_dir):
		with virtualenv(deployment_dir):
			run('python manage.py migrate --no-input --settings=__config.settings.{}'.format(environment))


def collect_static(deployment_dir, environment):
	with cd(deployment_dir):
		with virtualenv(deployment_dir):
			run('python manage.py collectstatic --no-input --settings=__config.settings.{}'.format(environment))

def create_symlink(deployment_dir, site_dir, project):
	with cd(site_dir):
		run('ln -sfn {deployment} {project}'.format(deployment=deployment_dir), project={project})


def create_project_gunicorn_startup(sites_dir, project, conf_file):	
	path = '/etc/systemd/system/{project}-gunicorn.service'.format(project=project)	
	with cd (sites_dir):
		run('ln -')
	sudo('touch {path}'.format(path=path))
	sudo ('>| {path}'.format(path=path))
	sudo("echo '{conf_file}' >> {path}".format(conf_file=conf_file, path=path))
	sudo('systemctl start {project}-gunicorn.service'.format(project=project))
	sudo('systemctl daemon-reload')


def create_project_nginx_conf(project, conf_file):
	path = '/etc/nginx/sites-available/{project}'.format(project=project)
	sudo('touch {path}'.format(path=path))
	sudo ('>| {path}'.format(path=path))
	sudo("echo '{conf_file}' >> {path}".format(conf_file=conf_file, path=path))
	sudo('ln -f -s {path} /etc/nginx/sites-enabled'.format(path=path))
	sudo('nginx -t')
	sudo('systemctl restart nginx')
	sudo("ufw allow 'Nginx Full'")


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


def gunicorn_conf_file(user, project, site_dir):
	pass


def nginx_conf_file(user, project, site_dir, domain):
	pass
	

def deploy(config, hosts):
	try:
		dir = execute(get_existing_directory, project=config['name'], hosts=hosts['user_hosts'])
		deployment_dir = '{root}/{project}/{dir}'.format(
			root=root_deploy_dir, 
			project=config['name'], 
			dir=dir
		)
		log_dir = '{log}/{project}'.format(
			log=root_log_dir, 
			project=config['name']
		)
		site_dir = root_site_dir
		print('Beginning a new deployment...')
		print('Step One: Create a new folder to deploy into...')
		execute(create_directories, deployment_dir, site_dir, log_dir, hosts=hosts['user_hosts'])
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