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


def upload():
    put(local_path, remote_path)


def restart_service():
    sudo("sudo systemctl restart %s" % service_name)
    sudo("sudo systemctl restart nginx")


if __name__ == "__main__":
    project_name = project_github.split("/")[-1]
    project_dir = "/home/%s/%s" % (user, project_name)
    service_name = "%s.service" % project_name

    local_path = "wsgi.py"
    remote_path = "%s/%s" % (project_dir, local_path)

    set_env()
    upload()
    restart_service()

# sudo dpkg-reconfigure tzdata
# 0 8 * * * /home/dev/scrapy-postgresql-sqlalchemy-api/env/bin/python /home/dev/scrapy-postgresql-sqlalchemy-api/crawler_run.py
