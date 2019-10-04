import os
import socket
import datetime
import uuid
import time
import shutil
import json
from subprocess import Popen

from scrimmage.db import DB
from scrimmage.utilities import *


class Server:
    def __init__(self):
        self.connections = list()
        self.database = DB()

        self.server_socket = None

        self.logs = list()

        self.max_simultaneous_runs = 4
        self.current_running = [x for x in range(self.max_simultaneous_runs)]

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(10)
        print('❤❤❤Welcome to HeartDB!❤❤❤')

        server_input = Thread(self.await_input, ())
        server_input.start()

        game_runner = Thread(self.runner_loop, ())
        game_runner.start()

        visualizer_runner = Thread(self.visualizer_loop, ())
        visualizer_runner.start()

        while True:
            connection, address = self.server_socket.accept()
            self.log(f'Connection from {address}.')

            client_thread = Thread(self.handle_client, (connection, address,))
            client_thread.start()

    def handle_client(self, connection, address):
        command = receive_data(connection)
        if command in ['register', '-r']:
            self.register_client(connection, address)
        connection.close()

    def register_client(self, connection, address):
        teamname = receive_data(connection)
        team_uuid = str(uuid.uuid4())
        # TODO: browse database to prevent repeat names
        if teamname in ['frankfurt', 'skungle dungus']:
            team_uuid = 'name already taken'
            self.log(f'Registration attempted for already taken teamname: {teamname}')
        else:
            self.log(f'Registering team: {teamname} with ID: {team_uuid}')
        send_data(connection, team_uuid)

    def await_input(self):
        print('Server is awaiting admin input.')
        while True:
            com = input('Ɛ>')
            self.log(f'Server command: {com}')
            # Exit command for shutting down the server
            if com == 'exit':
                os._exit(0)

            # Echo back the given string to the user, mostly for testing
            elif 'echo ' in com:
                print(com.replace('echo ', ''))

            # Display all the logs from the current server instance
            elif 'log' in com:
                for s in self.logs:
                    print(s)

            # Create a query of all entries in the database
            elif 'query' in com:
                tid = input('TID: ').strip()
                teamname = input('Team name: ').strip()

                if tid == '':
                    tid = None
                if teamname == '':
                    teamname = None

                print(*[str(e) + '\n' for e in self.database.query(tid, teamname)])

            # Show all entries in the database, equivalent to query with no parameters
            elif 'dump' in com:
                print(*[str(e) + '\n' for e in self.database.dump()])

            # Write a python command that will get executed
            elif 'exec' in com:
                try:
                    exec(input("WARNING: "))
                except Exception:
                    print('You did it wrong.')

    def runner_loop(self):
        while True:
            while len(self.current_running) == 0:
                pass

            num = self.current_running.pop(0)

            thr = Thread(self.internal, (None, num,))
            thr.start()

    def internal(self, client, number):
        try:
            # Run game
            self.log(f'Running client: {1}')
            if not os.path.exists(f'scrimmage/temp'):
                os.mkdir(f'scrimmage/temp')
            end_path = f'scrimmage/temp/{number}'
            if not os.path.exists(end_path):
                os.mkdir(end_path)

            shutil.copy('launcher.pyz', end_path)
            shutil.copy('first_client.py', end_path)
            shutil.copy('scrimmage/runner.bat', end_path)

            f = open(os.devnull, 'w')
            p = Popen('runner.bat', stdout=f, cwd=end_path, shell=True)
            stdout, stderr = p.communicate()

            with open(end_path + '/logs/results.json') as f:
                woop = json.load(f)

            shutil.rmtree(end_path)
            
        except Exception:
            pass

        self.current_running.append(number)

    def visualizer_loop(self):
        while True:
            # Pick game to run

            # Run game
            self.log(f'Visualizing game from client: {1}')
            time.sleep(30)
            pass

    def log(self, *args):
        for arg in args:
            self.logs.append(f'❤❤❤{datetime.datetime.now()}: {arg}❤❤❤')


if __name__ == '__main__':
    serv = Server()
    serv.start()
