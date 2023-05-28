import argparse
import subprocess
from datetime import datetime
from os import makedirs
from pathlib import Path
from time import sleep
from math import log10, ceil

from honeypot import HONEYPOTS
from ssh import SSH

TEST_CASES_FOLDER = "test-cases"
COMMAND_LOGS_FOLDER = "command-logs"
HONEYPOT_LOGS_FOLDER = "honeypot-logs"


def run_case(
    honeypot_name: str, case: Path, command_logs: Path, honeypot_logs: Path
) -> None:
    honeypot = HONEYPOTS[honeypot_name]
    honeypot.stop()
    honeypot.start()
    print("Honeypot started.")
    ssh = SSH(
        honeypot.container_name,
        2222,
        "root",
        honeypot.password,
        honeypot.container_name,
    )
    ssh.start()
    print("SSH started.")
    
    
    p = subprocess.Popen(
        honeypot.ssh_cmd,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        shell=True,
    )
    if p.stdin is None:
        print("Failed to start SSH connection.")
        return
    p.stdin.write(f"{SSH_START}\n".encode())
    p.stdin.write(f"{honeypot.password}\n".encode())
    print("SSH opened.")

    # Execute test case.
    with open(case, "br") as case_file:
        p.stdin.writelines(case_file.readlines())
    p.stdin.write(b"\n")
    print("Test case executed.")

    # Collect command logs amd close SSH.
    p.stdin.write(f"{SSH_STOP}\n".encode())
    with open(command_logs, "bw") as logs_file:
        logs_file.write(p.communicate()[0])
    print("SSH closed.")

    with open(honeypot_logs, "bw") as logs_file:
        logs_file.write(honeypot.logs())
    print("Honeypot logs extracted.")
    honeypot.stop()
    print("Honeypot stopped.")


def main(honeypot: str) -> None:
    test_cases_folder = Path(TEST_CASES_FOLDER)
    all_cases = list(test_cases_folder.iterdir())
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    command_logs_folder = (
        Path(COMMAND_LOGS_FOLDER).joinpath(honeypot).joinpath(timestamp)
    )
    honeypot_logs_folder = (
        Path(HONEYPOT_LOGS_FOLDER).joinpath(honeypot).joinpath(timestamp)
    )
    makedirs(command_logs_folder)
    makedirs(honeypot_logs_folder)
    all_cases_len = len(all_cases)
    padding = ceil(log10(all_cases_len))
    for no, case in enumerate(all_cases):
        print(f"Test case {no + 1:0>{padding}}/{all_cases_len}")
        command_logs = command_logs_folder.joinpath(case.name)
        honeypot_logs = honeypot_logs_folder.joinpath(case.name)
        run_case(honeypot, case, command_logs, honeypot_logs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("honeypot", choices=["cowrie", "kippo"])
    args = parser.parse_args()
    main(args.honeypot)
