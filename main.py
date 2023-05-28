import argparse
import subprocess
from datetime import datetime
from os import makedirs
from pathlib import Path
from time import sleep


class Honeypot:
    def __init__(self, name: str, image_name: str, shell: str, password: str) -> None:
        self.name = name
        self.container_name = f"auto-{self.name}"
        self.image_name = image_name
        self.password = password
        self.start_cmd = f"docker run -d --name {self.container_name} {self.image_name}"
        self.ssh_cmd = f"docker exec -i {self.container_name} {shell}"
        self.logs_cmd = f"docker logs {self.container_name}"
        self.stop_cmd = f"docker stop {self.container_name} && docker rm {self.container_name}"


HONEYPOTS = {
    "kippo": Honeypot(
        name="kippo",
        image_name="tomdesinto/kippo",
        shell="bash",
        password="123456",
    ),
    "cowrie": Honeypot(
        name="cowrie",
        image_name="cowrie/cowrie:latest",
        shell="sh",
        password=""
    ),
}

SSH_START = "ssh -T -o \"StrictHostKeyChecking=no\" -o \"KexAlgorithms=+diffie-hellman-group1-sha1\" -p 2222 root@127.0.0.1"
SSH_STOP = "exit"
HONEYPOT_SSH_STOP = "exit"

TEST_CASES_FOLDER = "test-cases"
COMMAND_LOGS_FOLDER = "command-logs"
HONEYPOT_LOGS_FOLDER = "honeypot-logs"


def run_case(honeypot_name: str, case: Path, command_logs: Path, honeypot_logs: Path) -> None:
    # Cleanup if previous test is still open.
    honeypot = HONEYPOTS[honeypot_name]
    p = subprocess.Popen(honeypot.stop_cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    pre_cleanup_output = p.communicate()[0].decode()

    # Start docker with the honeypot.
    p = subprocess.Popen(honeypot.start_cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    start_output = p.communicate()[0].decode()
    print("Honeypot started.")

    # Open SSH to the container, then SSH to the honeypot from inside the container.
    sleep(1) # Allow ssh to start
    p = subprocess.Popen(honeypot.ssh_cmd, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    if p.stdin is None:
        print("Failed to start SSH connection.")
        return
    p.stdin.write(f'{SSH_START}\n'.encode())
    p.stdin.write(f'{honeypot.password}\n'.encode())
    print("SSH opened.")

    # Execute test case.
    with open(case, 'br') as case_file:
        p.stdin.writelines(case_file.readlines())
    p.stdin.write(b"\n")
    print("Test case executed.")

    # Collect command logs amd close SSH.
    p.stdin.write(f'{SSH_STOP}\n'.encode())
    p.stdin.write(f'{HONEYPOT_SSH_STOP}\n'.encode())
    with open(command_logs, 'bw') as logs_file:
        logs_file.write(p.communicate()[0])
    print("SSH closed.")

    # Collect honeypot logs.
    p = subprocess.Popen(honeypot.logs_cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    with open(honeypot_logs, 'bw') as logs_file:
        logs_file.write(p.communicate()[0])
    print("Honeypot logs extracted.")

    # Close honeypot.
    p = subprocess.Popen(honeypot.stop_cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    post_cleanup_output = p.communicate()[0].decode()
    print("Honeypot stopped.")


def main(honeypot: str) -> None:
    test_cases_folder = Path(TEST_CASES_FOLDER)
    all_cases = list(test_cases_folder.iterdir())
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    command_logs_folder = Path(COMMAND_LOGS_FOLDER).joinpath(honeypot).joinpath(timestamp)
    honeypot_logs_folder = Path(HONEYPOT_LOGS_FOLDER).joinpath(honeypot).joinpath(timestamp)
    makedirs(command_logs_folder)
    makedirs(honeypot_logs_folder)
    for case in all_cases:
        command_logs = command_logs_folder.joinpath(case.name)
        honeypot_logs = honeypot_logs_folder.joinpath(case.name)
        run_case(honeypot, case, command_logs, honeypot_logs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("honeypot", choices=["cowrie", "kippo"])
    args = parser.parse_args()
    main(args.honeypot)
