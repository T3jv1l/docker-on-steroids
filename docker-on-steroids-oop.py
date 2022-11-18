import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings(action='ignore', category=CryptographyDeprecationWarning)
import docker
import time
import argparse
import sys
from dotenv import main
import os
import paramiko

class DockeronSteroids():
    def __init__(self) -> None:
        """Construct all the necessary attributes"""
        self.docker_env = docker.from_env()
        self.parser = argparse.ArgumentParser()

    def __setArgs(self):
        """Setting the arguments"""
        self.parser.add_argument('-s',type=str, required=False,
                     help='search all docker-compose.yml file', metavar=' --search')
        self.parser.add_argument("-a", "--all" ,help="purge all docker containers",
                    action="store_true")

        subparser = self.parser.add_subparsers(dest='remote')
        
        ssh = subparser.add_parser('ssh-remove')
        ssh.add_argument('--host', type=str ,required=True, help="Host require", metavar='10.x.x.x.x')
        ssh.add_argument('--port', type=str ,required=True, help="Port require", metavar='22')

        self.remote_ssh = self.parser.parse_args()

    def __connect_remote(self, host, user, password=None, port=None,timeout=4):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if password is not None:
            client.connect(hostname=host, username=user, password=password, port=port, timeout=timeout)
        return client

    def __check(self):
        """Checking the number of arguments"""
        if len(sys.argv) <= 1:
            sys.argv.append('--help')

    def __display_image(self):
        """Displaying all the docker images"""
        list = self.docker_env.images.list(all=True)

        if list == []:
            return "{'Image list is empty': None}"
        else:
            return list 

    def __remove_image(self):
        """Removing the docker image"""
        img = self.docker_env.images.prune(filters={'dangling': False})
        return img

    def __remove_containers_inactive(self):
        """Removing the inactive docker container"""
        cont = self.docker_env.containers.prune()
        return cont 

    def __remove_networks(self):
        """Removing the docker network"""
        net = self.docker_env.networks.prune()
        return net

    def __remove_volumes(self):
        """Removing the docker volumes"""
        time.sleep(0.5)
        vol = self.docker_env.volumes.prune()
        return vol 

    def __remove_containers_active(self):
        """Removing the active docker container"""
        containers = self.docker_env.containers.list(all=True)
        
        if containers == []:
            return "{'Active Container list is empty': None}"
        else:
            for cont in containers:
                cont.remove(force=True)
            return containers
    
    def __remove_remote(self):
        """Calling all the fucntion to remove remote all the docker which is running"""
        env_path='.env'
        main.load_dotenv(dotenv_path=env_path)
        if self.remote_ssh.remote == 'ssh-remove':
            try:
                user = os.getenv('SECRET_USER')
                password = os.getenv('SECRET_PASSWORD')
                host = self.remote_ssh.host
                port = self.remote_ssh.port
        
                ssh_connect_remote = self.__connect_remote(host=host, user=user, password=password, port=port)
                
                stdin, stdout, stderr = ssh_connect_remote.exec_command("docker system prune -a --force")
                print(stdout.read().decode())
                stdin, stdout, stderr = ssh_connect_remote.exec_command("docker container stop $(docker container ls -aq)")
                print(stdout.read().decode())
                stdin, stdout, stderr = ssh_connect_remote.exec_command("docker network prune --force")
                print(stdout.read().decode())
                stdin, stdout, stderr = ssh_connect_remote.exec_command("docker container rm $(docker container ls -aq)")
                print(stdout.read().decode())
                stdin, stdout, stderr = ssh_connect_remote.exec_command("docker rmi $(docker images -aq)")
                print(stdout.read().decode())
               
                ssh_connect_remote.close()
        
            except paramiko.AuthenticationException:
                print ("[?] We had an authentication error!")

    def __remove(self):
        """Calling all the functions responsable for purging the docker"""
        print(self.__display_image())
        print(self.__remove_networks())
        print(self.__remove_containers_inactive())
        print(self.__remove_volumes())
        print(self.__remove_containers_active())
        print(self.__remove_image())


    def __arguments(self, options):
        print(options)
        if options.all:
            self.__remove()
            exit()
        elif options.remote:
            self.__remove_remote()
            exit()

    def run(self):
        self.__setArgs()
        self.__check()
        self.options = self.parser.parse_args()
        self.__arguments(self.options)

if __name__ == '__main__':
    test = DockeronSteroids()
    test.run()
