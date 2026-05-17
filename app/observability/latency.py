from contextlib import contextmanager
import time

@contextmanager
def latency_timer():
    start = time.perf_counter()
    data = {}
    yield data
    data["latency_ms"] = int((time.perf_counter() - start) * 1000)
