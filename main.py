import argparse
from pathlib import Path
import subprocess
from os import makedirs
from datetime import datetime
from time import sleep

HONEYPOT_START = {
    "kippo": "docker run -d --name auto-kippo tomdesinto/kippo",
    "cowrie": "docker run -d --name auto-cowrie cowrie/cowrie:latest",
}
HONEYPOT_SSH_START = {
    "kippo": "docker exec -i auto-kippo bash",
    "cowrie": "docker exec -i auto-cowrie sh",
}
HONEYPOT_PASSWORD = {"kippo": "123456", "cowrie": ""}
HONEYPOT_EXTRACT_LOGS = {"kippo": "docker logs auto-kippo", "cowrie": "docker logs auto-cowrie"}
HONEYPOT_STOP = {
    "kippo": "docker stop auto-kippo && docker rm auto-kippo",
    "cowrie": "docker stop auto-cowrie && docker rm auto-cowrie",
}

SSH_START = "ssh -T -o \"StrictHostKeyChecking=no\" -o \"KexAlgorithms=+diffie-hellman-group1-sha1\" -p 2222 root@127.0.0.1"
SSH_STOP = "exit"
HONEYPOT_SSH_STOP = "exit"

TEST_CASES = "test-cases"
RESULTS = "results"
COMMAND_LOGS_FOLDER = "command-logs"
HONEYPOT_LOGS_FOLDER = "honeypot-logs"


def run_case(honeypot: str, case: Path, command_logs: Path, honeypot_logs: Path):
    # Cleanup if previous test is still open.
    p = subprocess.Popen(HONEYPOT_STOP[honeypot], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    pre_cleanup_output = p.communicate()[0].decode()
    
    # Start docker with the honeypot.
    p = subprocess.Popen(HONEYPOT_START[honeypot], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    start_output = p.communicate()[0].decode()
    print("Honeypot started.")
    
    # Open SSH to the container, then SSH to the honeypot from inside the container.
    sleep(1) # Allow ssh to start
    p = subprocess.Popen(f'{HONEYPOT_SSH_START[honeypot]}', stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    p.stdin.write(f'{SSH_START}\n'.encode())
    p.stdin.write(f'{HONEYPOT_PASSWORD[honeypot]}\n'.encode())
    print("SSH opened.")
    
    # Execute test case.
    with open(case, 'br') as case:
        p.stdin.writelines(case.readlines())
    p.stdin.write(b"\n")
    print("Test case executed.")
    
    # Collect command logs amd close SSH.
    p.stdin.write(f'{SSH_STOP}\n'.encode())
    p.stdin.write(f'{HONEYPOT_SSH_STOP}\n'.encode())
    with open(command_logs, 'bw') as logs:
        logs.write(p.communicate()[0])
    print("SSH closed.")
    
    # Collect honeypot logs.
    p = subprocess.Popen(HONEYPOT_EXTRACT_LOGS[honeypot], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    with open(honeypot_logs, 'bw') as logs:
        logs.write(p.communicate()[0])
    print("Honeypot logs extracted.")
    
    # Close honeypot.
    p = subprocess.Popen(HONEYPOT_STOP[honeypot], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    post_cleanup_output = p.communicate()[0].decode()
    print("Honeypot stopped.")


def main(honeypot: str):
    test_cases_folder = Path(TEST_CASES)
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

