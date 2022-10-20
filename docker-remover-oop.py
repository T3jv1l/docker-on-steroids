from email.message import Message
import docker
import time
import argparse
import sys
import paramiko
import os
from dotenv import load_dotenv

class DockeronSteroids():
    def __init__(self) -> None:
        """Construct all the necessary attributes"""
        load_dotenv()
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
        ssh.add_argument('--user', type=str ,required=True, help="Username require", metavar='admin')
        ssh.add_argument('--port', type=str ,required=True, help="port require", metavar='22')

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

    def run(self):
        self.__setArgs()
        self.__check()
        self.options = self.parser.parse_args()
        self.__arguments(self.options)

if __name__ == '__main__':
<<<<<<< HEAD
=======

>>>>>>> 2199fe9160f4f38b3bd511fa2295197d20c3e3dc
    test = DockeronSteroids()
    test.run()
