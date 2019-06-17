from fabric.api import env, run, sudo

from A_config import *


def set_env():
    env.host_string = server_domain
    env.user = "root"
    if root_password:
        env.password = root_password
    else:
        env.key_filename = root_keyfile


def main():
    set_env()
    sudo("adduser %s" % user)
    sudo("usermod -aG sudo %s" % user)
    run("ufw app list")
    run("ufw allow OpenSSH")
    run("ufw enable")
    run("ufw status")


if __name__ == "__main__":
    main()
