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


def main():
    set_env()

    sudo("sudo apt-get update")
    sudo("sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx")

    sudo('sudo -u postgres psql -c "create database %s;"' % db_name)
    sudo('sudo -u postgres psql -c "CREATE USER %s WITH PASSWORD \'%s\';"' % (db_user, db_password))
    sudo('sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s;"' % (db_name, db_user))


if __name__ == "__main__":
    main()
