import io
import os
import subprocess
import sys


def _log_subprocess_output(pipe):
    for line in iter(pipe.readline, b""):  # b'\n'-separated lines
        print(line.decode("utf-8").replace("\r\n", ""))


def run_and_read_line(command: str, shell=False):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell)
    return io.TextIOWrapper(proc.stdout, encoding="utf-8").read().replace("\n", "")


def run_shell_command(command: str, base_path: str = os.getcwd(), shell=False):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=base_path, shell=shell)
    with proc.stdout:
        _log_subprocess_output(proc.stdout)

    exitcode = proc.wait()  # 0 means success

    if exitcode > 0:
        sys.exit(exitcode)
