import os


from fabric.contrib.files import append, exists, sed, put
from fabric.api import env, run, sudo

from A_config import *


def set_env():
    env.host_string = server_domain
    env.user = user
    if user_keyfile:
        env.key_filename = user_keyfile
        env.password = user_password
    else:
        env.password = user_password


def update():
    run('cd %s && git pull' % project_dir)
    run("%s/bin/pip install -r %s/req.txt" % (project_env, project_dir))
    sudo("sudo systemctl restart %s" % service_name)
    sudo("sudo systemctl restart nginx")


if __name__ == "__main__":
    project_name = project_github.split("/")[-1]
    project_dir = "/home/%s/%s" % (user, project_name)
    project_env = os.path.join(project_dir, 'env')
    service_name = "%s.service" % project_name

    set_env()
    update()
