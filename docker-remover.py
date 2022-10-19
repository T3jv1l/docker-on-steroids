import docker
import time
import argparse
import sys
import paramiko
from dotenv import load_dotenv
import os

load_dotenv()

docker = docker.from_env()

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='remote')

ssh = subparser.add_parser('ssh-remove')

parser.add_argument('-all',type=str, required=False, help="purge all docker containers", metavar='purge')
parser.add_argument('-search',type=str, required=False, help='search all docker-compose.yml file', metavar='docker-compose.yml')

ssh.add_argument('--host', type=str ,required=True, help="Host require", metavar='10.x.x.x.x')
ssh.add_argument('--user', type=str ,required=True, help="Username require", metavar='admin')
# ssh.add_argument('--password', type=str ,required=True, help="Password require", metavar='password')
ssh.add_argument('--port', type=str ,required=True, help="port require", metavar='22')

if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()

def connect(host, user, password=None, port=None,timeout=4):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if password is not None:
        client.connect(hostname=host, username=user, password=password, port=port, timeout=timeout)
    return client

def display_image():
    list = docker.images.list(all=True)

    if list == []:
        return "{'Image list is empty': None}"
    else:
        return list 

def remove_image():
    img = docker.images.prune(filters={'dangling': False})
    return img

def remove_containers_inactive():
    cont = docker.containers.prune()
    return cont 

def remove_networks():
    net = docker.networks.prune()
    return net

def remove_volumes():
    time.sleep(0.5)
    vol = docker.volumes.prune()
    return vol 

def remove_containers_active():
    containers = docker.containers.list(all=True)
    
    if containers == []:
        return "{'Active Container list is empty': None}"
    else:
        for cont in containers:
            cont.remove(force=True)
        return containers

def argument():
    if options.all == "purge":
        print(display_image())
        print(remove_networks())
        print(remove_containers_inactive())
        print(remove_volumes())
        print(remove_containers_active())
        print(remove_image())
        
        exit()
        
    elif options.remote == 'ssh-remove':
        try:
            env_path='.env'
            load_dotenv(dotenv_path=env_path)
            # password = options.password
            password = os.getenv('PASSWORD')
            user = options.user
            host = options.host
            port = options.port

            s = connect(host=host, user=user, password=password, port=port)

            stdin, stdout, stderr = s.exec_command("docker system prune -a --force")
            print(stdout.read().decode())
            stdin, stdout, stderr = s.exec_command("docker container stop $(docker container ls -aq)")
            print(stdout.read().decode())
            stdin, stdout, stderr = s.exec_command("docker network prune --force")
            print(stdout.read().decode())
            stdin, stdout, stderr = s.exec_command("docker container rm $(docker container ls -aq)")
            print(stdout.read().decode())
            stdin, stdout, stderr = s.exec_command("docker rmi $(docker images -aq)")
            print(stdout.read().decode())
            s.close()
        except paramiko.AuthenticationException:
            print ("[?] We had an authentication error!")

def search_docker_compose():
        if options.search == "docker-compose.yml":
            with open('docker_compose_location.txt', 'w') as f:
                for root, dirs, files in os.walk("/"):
                    for file_docker in files:
                        if file_docker.endswith("docker-compose.yml"):
                            print(os.path.join(root, file_docker), file=f)
                else:
                    exit()

if __name__ == '__main__':
    argument()
    search_docker_compose()
    # print(remove_containers_active())
    # print(remove_image())
