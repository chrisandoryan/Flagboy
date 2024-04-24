import os
import socket
import paramiko
import secrets
from dotenv import load_dotenv
load_dotenv(override=True)

BASE_URL = os.environ["CTFD_URL"]
TOKEN = os.environ["CTFD_TOKEN"]

def check_services(target, port_list):
    success_count = 0
    pl = port_list.copy()

    ssh_port = 22
    if "ssh_port" in target:
        ssh_port = target['ssh_port']
        pl.append(ssh_port)

    for p in pl:
        print(f"Checking {target['ip_address']}:{p}")
        result = get_heartbeat(target['ip_address'], p)
        if (result):
            print("[+] Alive")
            success_count += 1
        else:
            print("[-] Dead")
    
    return success_count > 0

def get_heartbeat(target_host, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((target_host, target_port))
    return result == 0

def inject_flag(target, flag, mode="ROOT"):
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

    print(ssh_username, ssh_password)

    ssh_port = 22
    if "ssh_port" in target:
        ssh_port = target['ssh_port']
        print(f"[!] Switching SSH port to {ssh_port}")

    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        s.connect(target['ip_address'], ssh_port, ssh_username, ssh_password)
        command = "echo '%s' | sudo -S /bin/sh -c \"echo '%s' > %s\"; chown %s:%s %s" % (ssh_password, flag, flag_path, username, username, flag_path)
        print(f"\t[o] {command}")

        stdin, stdout, stderr = s.exec_command(command)
        for line in stdout.readlines():
            print(f"[!!!] {line}")
        s.close()

        recv_status = stdout.channel.recv_exit_status()
        print(f"[!!!] Recv Status: {recv_status}")
        return recv_status >= 0
    except Exception as e:
        print(f"[!!!] SSH Error!")
        print(e)
        
        return False
    

def change_box_password(target, new_password, mode="ROOT"):
    if mode == "ROOT":
        username = "root"
    else:
        username = os.environ["BOX_USER_NAME"]

    ssh_username = os.environ["BOX_SA_NAME"]
    ssh_password = os.environ["BOX_SA_PASSWORD"]

    ssh_port = 22
    if "ssh_port" in target:
        ssh_port = target['ssh_port']
        print(f"[!] Switching SSH port to {ssh_port}")

    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        s.connect(target['ip_address'], ssh_port, ssh_username, ssh_password)
        
        # Change the password for 'root'
        stdin, stdout, stderr = s.exec_command(f'echo -e "{new_password}\\n{new_password}" | passwd {username}')
        print(stdout.read().decode())
        print(stderr.read().decode())

        # Close the SSH connection
        s.close()

        recv_status = stdout.channel.recv_exit_status()
        print(f"[!!!] Recv Status: {recv_status}")
        return recv_status >= 0
    except Exception as e:
        print(f"[!!!] SSH Error!")
        print(e)
        
        return False