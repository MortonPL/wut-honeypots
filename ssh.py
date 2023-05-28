import subprocess

from docker import run_cmd


class SSH:
    def __init__(self, host, port, user, password, honeypot_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.docker_start_cmd = f"docker run -d --name auto-sshpass --link={honeypot_name} --expose={self.port} $(docker build -q .)"
        self.docker_stop_cmd = "docker stop auto-sshpass && docker rm auto-sshpass"
        self.ssh_start_cmd = f'sshpass -p {self.password} -T -o "StrictHostKeyChecking=no" -o "KexAlgorithms=+diffie-hellman-group1-sha1" -p {self.port} {user}@{self.host}'
        self.ssh_stop_cmd = "exit"

    def start(self):
        return run_cmd(self.docker_start_cmd)

    def exec_local(self, file):
        pass

    def exec_remote(self, file):
        pass

    def stop(self):
        return run_cmd(self.docker_start_cmd)
