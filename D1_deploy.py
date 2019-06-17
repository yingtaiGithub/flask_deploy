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


def initial_install():
    sudo('sudo apt-get update && sudo apt-get -y upgrade')
    sudo('sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools')
    run('git clone %s' % project_github)


def make_virtualenv():
    sudo("sudo apt install python3-venv")
    run("cd %s && python3.6 -m venv env" % project_dir)
    run("%s/bin/pip install wheel" % project_env)
    run("%s/bin/pip install -r %s/req.txt" % (project_env, project_dir))
    run("%s/bin/pip install gunicorn" % project_env)


def gunicorn_service():
    service_folder = "/etc/systemd/system"
    service_name = "%s.service" % project_name

    script = """'[Unit]
        Description=Gunicorn instance to serve {project_name}
        After=network.target

        [Service]
        User={username}
        Group=www-data
        WorkingDirectory={project_dir}
        Environment="PATH={virtualenv}/bin"
        ExecStart={virtualenv}/bin/gunicorn --workers 3 --bind unix:{project_name}.sock -m 007 wsgi:app

        [Install]
        WantedBy=multi-user.target'""".format(
        project_name=project_name,
        username=user,
        project_dir=project_dir,
        virtualenv=project_env
    )

    sudo('sudo echo {} > {}/{}'.format(script, service_folder, service_name))
    sudo('sudo systemctl daemon-reload')
    sudo('sudo systemctl start {}'.format(project_name))
    sudo('sudo systemctl enable {}'.format(project_name))


def nginx_conf():
    conf_file = "/etc/nginx/sites-available/{}".format(project_name)
    script = """'server {{
        listen 80;
        server_name {domain};

        location / {{
            include proxy_params;
            proxy_pass http://unix:{project_dir}/{project_name}.sock;
        }}
    }}'""".format(
        domain=server_domain,
        project_dir=project_dir,
        project_name=project_name
    )

    sudo('sudo echo {} > {}'.format(script, conf_file))
    try:
        sudo('sudo ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled'.format(project_name))
    except:
        pass

    sudo('sudo systemctl restart nginx')
    sudo('sudo ufw delete allow 5000')
    sudo("sudo ufw allow 'Nginx Full'")

    # sudo('sudo ufw allow 5000')


def deploy():
    initial_install()
    make_virtualenv()
    gunicorn_service()
    nginx_conf()


if __name__ == "__main__":
    project_name = project_github.split("/")[-1]
    project_dir = "/home/%s/%s" % (user, project_name)
    project_env = os.path.join(project_dir, 'env')

    set_env()
    deploy()
