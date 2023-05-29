import subprocess


def run_cmd(cmd: str):
    p = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        shell=True,
    )
    return p.communicate()[0].decode()
