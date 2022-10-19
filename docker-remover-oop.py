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
        load_dotenv()
        self.parser = argparse.ArgumentParser()

    def __setArgs(self):

        self.parser.add_argument('-all',type=str, required=False, help="purge all docker containers", metavar='purge')
        self.parser.add_argument('-search',type=str, required=False, help='search all docker-compose.yml file', metavar='docker-compose.yml')

        subparser = self.parser.add_subparsers(dest='remote')
        
        ssh = subparser.add_parser('ssh-remove')
        ssh.add_argument('--host', type=str ,required=True, help="Host require", metavar='10.x.x.x.x')
        ssh.add_argument('--user', type=str ,required=True, help="Username require", metavar='admin')
        ssh.add_argument('--port', type=str ,required=True, help="port require", metavar='22')

    def __check(self):
        if len(sys.argv) <= 1:
            sys.argv.append('--help')

    def run(self):
        self.__setArgs()
        self.__check()
        self.options = self.parser.parse_args()

if __name__ == '__main__':
    load_dotenv()

    test = DockeronSteroids()
    test.run()