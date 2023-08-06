import time
import contextlib
import sys


# simple timers to provide intermediate during prints.
# This is context
class PerfBenchmark:
    def __init__(self, name, log_print=print):
        self.name = name
        self.log_print = log_print
        self.start = None
        self.last_step = None
        self.dur = 0

    def __enter__(self):
        self.start = time.time()
        self.last_step = self.start
        return self

    def print(self, step):
        now = time.time()
        dur = now - self.last_step
        self.log_print("{0} takes: {1:.3f} seconds".format(step, dur))
        self.last_step = now
        return dur

    def curr_step(self):
        return time.time() - self.last_step

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dur = time.time() - self.start
        self.log_print(f"{self.name} takes: {self.dur:.3f} seconds")
        return False  # This will let exception pass through this class to callers


# This is another way to avoid class and you don't care the total time in return.
@contextlib.contextmanager
def perf_bm(name, log_print=print):
    pbm = PerfBenchmark(name, log_print=log_print)
    try:
        pbm.__enter__()
        yield pbm
        pbm.__exit__(None, None, None)
    except Exception as e:
        if not pbm.__exit__(type(e), e.args, sys.exc_info()[2]):
            raise e
