import subprocess


def run_cmd(command):
    return subprocess.check_output(command, shell=True)
