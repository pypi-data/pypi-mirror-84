import subprocess
import sys
import time
import threading


# https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
def run_cmd(cmd, timeout=0):
    # same as subprocess.check_output
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if timeout:  # This is to deal with 0: communicate() takes None is no timeout.
        stdout, stderr = proc.communicate(timeout=timeout)
    else:
        stdout, stderr = proc.communicate()

    reply = stdout.decode('utf-8') + stderr.decode('utf-8')
    return proc.returncode, reply


# timeout is None: no timeout
def run_wto(cmd, timeout=0, check_timeout_interval=1):
    # need to reroute stderr in proc to stdout, otherwise won't get msg
    # do not set shell=True, since we can't kill it for timeout
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)

    if timeout:
        thread = threading.Thread(target=_proc_monitor,
                                  args=(proc, timeout, check_timeout_interval))
        thread.daemon = True
        thread.start()

    reply = ''
    while proc.poll() is None:
        lines = proc.stdout.readlines()
        for line in lines:
            reply += line
            print(line)
        sys.stdout.flush()

    proc.stdout.close()
    proc.terminate()

    return proc.returncode, reply


def run_progress(exe, timeout=None, check_timeout_interval=1):
    # try:
    # need to reroute stderr in proc to stdout, otherwise won't get msg
    # do not set shell=True, since we can't kill it for timeout
    proc = subprocess.Popen(exe, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)
    if timeout:
        thread = threading.Thread(target=_proc_monitor,
                                  args=(proc, timeout, check_timeout_interval))
        thread.daemon = True
        thread.start()

    while proc.poll() is None:
        lines = proc.stdout.readlines()
        for line in lines:
            yield line.replace('\n', '')
        sys.stdout.flush()

    proc.stdout.close()
    proc.terminate()

    yield proc.returncode


def _proc_monitor(proc, timeout, check_timeout_interval):
    now = time.time()
    while time.time() - now < timeout:
        print(f'sleeping: {proc.returncode}')
        time.sleep(check_timeout_interval)

    if proc.returncode is None:
        print('monitor: process timed out')
        proc.terminate()
