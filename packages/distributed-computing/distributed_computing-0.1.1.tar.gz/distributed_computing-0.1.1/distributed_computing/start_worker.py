import argparse
import multiprocessing
import os
import subprocess
import tempfile
from multiprocessing import Process

import psutil
import requests
from redis import Redis

from Experiments.common.distributed_computing.client import run_pool_client
from Experiments.common.distributed_computing.server import run_pool_server
from Experiments.global_config import config


def _start_redis():

    try:
        Redis('localhost', password=config["worker_pool_redis_server_password"], socket_connect_timeout=1).ping()
    except:
        _, conf_file = tempfile.mkstemp()

        with open(conf_file, 'w') as f:
            f.write(f'requirepass {config["worker_pool_redis_server_password"]}')

        FNULL = open(os.devnull, 'w')

        print('Redis server is started.')

        return subprocess.Popen(['redis-server', conf_file, '--protected-mode no'], stdout=FNULL)


def start_workers_server():

    if is_server_running():
        print('A server is already running on this machine')
        return lambda: 0, lambda: 0

    redis_process = _start_redis()

    print('Starting workers pool server.')
    pool_server = Process(target=run_pool_server)
    pool_server.start()

    def terminate():
        pool_server.terminate()

        if redis_process is not None:
            redis_process.terminate()

    return terminate, lambda: pool_server.join()


def start_workers_client(address=None, port=None, violent_exit=True):

    if is_client_running():
        print('A client is already running on this machine')
        return lambda: 0, lambda: 0

    address = address or 'localhost'
    port = port or config['worker_pool_server_port']

    print('Starting workers pool client.')

    client = Process(target=run_pool_client, args=(address, port, violent_exit))
    client.start()

    return lambda: client.terminate(), lambda: client.join()


def start_local_workers_pool():

    server_terminator, server_waiter = start_workers_server()
    client_terminator, client_waiter = start_workers_client()

    def terminate():
        server_terminator()
        client_terminator()

    def wait():
        server_waiter()
        client_waiter()

    print('\n' + '\033[36m*\033[0m' * 90)
    print('\033[1mTo start a workers client in another node, type:\033[0m')
    ip = requests.get('https://api.ipify.org').text
    port = config['worker_pool_server_port']
    print(f'\033[92mpython Experiments/common/distributed_computing/start_worker.py -p {port} -a {ip}\033[0m')
    print('\033[36m*\033[0m' * 90 + '\n')

    return terminate, wait


def is_server_running():
    return 'ExperimentWorkersServer' in [p.name() for p in psutil.process_iter()]


def is_client_running():
    return 'ExperimentWorkersClient' in [p.name() for p in psutil.process_iter()]


parser = argparse.ArgumentParser()

parser.add_argument("-d", "--head", action="store_true", help='Indicate that this is the head node')
parser.add_argument("-s", "--server-only", action="store_true", help='Run only the server')
parser.add_argument("-a", "--address", required=False, help='Head node address')
parser.add_argument("-p", "--port", required=False, type=int, help='Head node port')


if __name__ == '__main__':

    multiprocessing.set_start_method('spawn')

    args = parser.parse_args()

    port = args.port or config['worker_pool_server_port']
    address = args.address or config['worker_pool_server_address']

    if args.head and args.server_only:
        terminate, wait = start_workers_server()

    elif args.head:
        terminate, wait = start_local_workers_pool()

    else:
        terminate, wait = start_workers_client(address, port, True)

    wait()
