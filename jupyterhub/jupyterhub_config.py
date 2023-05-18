# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import os, sys
import shutil

# https://github.com/jupyterhub/jupyterhub/tree/main/examples/bootstrap-script
# relevant only to populate content in spawned container.
#def create_dir_hook(spawner):
#    username = spawner.user.name # get the username
#    data_path = os.path.join( '/disk01/jupyter/' , username ) #path on the jupytherhub host, create a folder based on username if not exists
#    print("Running ----> ")
#    print("username : ", username)
#    print("data_path : ", data_path)
#    if not os.path.exists(data_path):
#        os.mkdir(data_path, 0o755)
#        print("PASS")
#        shutil.chown(data_path, user=username, group='users')
#pass

c = get_config()
c.JupyterHub.log_level = 10

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
            # "admin:users", # if using --cull-users
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    }
]

## Authenticator
# https://blog.jupyter.org/simpler-authentication-for-small-scale-jupyterhubs-with-nativeauthenticator-999534c77a09
#c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
#c.NativeAuthenticator.open_signup = True
#c.Authenticator.admin_users = { 'shoh' }

#c.NativeAuthenticator.check_common_password = True

#c.NativeAuthenticator.allowed_failed_logins = 3
#c.NativeAuthenticator.seconds_before_next_try = 1200
#################################################################

from oauthenticator.github import GitHubOAuthenticator
c.JupyterHub.authenticator_class = GitHubOAuthenticator

c.GitHubOAuthenticator.create_system_users = True

c.Authenticator.allowed_users = allowed_users = set()
c.JupyterHub.admin_users = admin = set()

c.MyOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
c.MyOAuthenticator.client_id = os.environ['OAUTH_CLIENT_ID']
c.MyOAuthenticator.client_secret = os.environ['OAUTH_CLIENT_SECRET']

#################################################################

#from oauthenticator.github import LocalGitHubOAuthenticator
#c.JupyterHub.authenticator_class = LocalGitHubOAuthenticator

#c.LocalGitHubOAuthenticator.create_system_users = True
#c.Authenticator.allowed_users = allowed_users = set()
#c.JupyterHub.admin_users = admin = set()

######################################################################

join = os.path.join
here = os.path.dirname(__file__)
root = os.environ.get('OAUTHENTICATOR_DIR', here)
sys.path.insert(0, root)

with open(join(root, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        allowed_users.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

#ssl config
#https://hackmd.io/@DanielChen/Sy81P-Aw4?type=viewe
# openssl req -x509 -nodes -days 3650 -newkey rsa:1024 -keyout /etc/jupyterhub/certificate/key.pem -out /etc/jupyterhub/certificate/cert.pem
ssl = '/etc/jupyterhub/certificate/'
keyfile = join(ssl, 'key.pem')
certfile = join(ssl, 'cert.pem')
if os.path.exists(keyfile): c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile): c.JupyterHub.ssl_cert = certfile

print("c.Authenticator.allowed_users : ", c.Authenticator.allowed_users)
print("c.JupyterHub.admin_users : ", c.JupyterHub.admin_users)

#################################################################

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.debug = True
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
## attach the hook functions to the spawner
##c.Spawner.pre_spawn_hook = create_dir_hook
c.DockerSpawner.volumes = { 
    'jupyterhub-user-{username}' : notebook_dir , 
    '/disk01/jupyter/{username}' : notebook_dir + '/work' ,
    '/disk01/cms-open-data'      : notebook_dir + '/data'
}

# Remove containers once they are stopped.
c.DockerSpawner.remove_containers = True

# Other stuff
c.Spawner.cpu_limit = 7.0
c.Spawner.mem_limit = '8G'

# Advanced USER
#c.DockerSpawner.extra_host_config = {
#    'mem_limit': '2g',
#    'memswap_limit': -1,
##    #'mem_swappiness': 1,
##    #'cpu_period': 100000,
##    #'cpu_quota': 250000
#}

## Services
# terminate idle jupyter session after 1 hour
c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600",
        ],
        # "admin": True,
    }
]
