import os
import socket
import paramiko
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.environ["CTFD_URL"]
TOKEN = os.environ["CTFD_TOKEN"]

def get_heartbeat(target_host, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((target_host, target_port))
    return result == 0

def inject_flag(target_host, flag, mode="ROOT"):
    if mode == "ROOT":
        username = "root"
        password = os.environ["BOX_ROOT_PASSWORD"]
        flag_path = os.environ["BOX_ROOT_FLAG_PATH"]
    else:
        username = os.environ["BOX_USER_NAME"]
        password = os.environ["BOX_USER_PASSWORD"]
        flag_path = os.environ["BOX_USER_FLAG_PATH"]

    ssh_username = os.environ["BOX_SA_NAME"]
    ssh_password = os.environ["BOX_SA_PASSWORD"]

    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    s.connect(target_host, 22, ssh_username, ssh_password)
    command = "echo '%s' > %s; chown %s:%s %s" % (flag, flag_path, username, username, flag_path)
    print(command)

    stdin, stdout, stderr = s.exec_command(command)
    for line in stdout.readlines():
        print(line)
    s.close()
    return stdout.channel.recv_exit_status() == -1