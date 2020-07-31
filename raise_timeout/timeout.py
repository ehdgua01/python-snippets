"""

>>> with timeout_contextmanager(0.5):
...     while True:
...         pass
...
timeout
>>> @timeout_decorator(0.5)
... def run_forever():
...     while True:
...         pass
...
>>> run_forever()
timeout
"""
import signal
from contextlib import contextmanager
from typing import Union, Any

Number = Union[int, float]


def raise_timeout(signum, frame) -> None:
    raise TimeoutError()


@contextmanager
def timeout_contextmanager(sec: Number) -> None:
    signal.signal(signal.SIGALRM, raise_timeout)
    signal.setitimer(signal.ITIMER_REAL, sec)
    try:
        yield
    except TimeoutError:
        print("timeout")
    finally:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def timeout_decorator(sec: Number) -> Any:
    def wrapper(func) -> Any:
        def container(*args, **kwargs) -> Any:
            signal.signal(signal.SIGALRM, raise_timeout)
            signal.setitimer(signal.ITIMER_REAL, sec)
            try:
                return func(*args, **kwargs)
            except TimeoutError:
                print("timeout")
            finally:
                signal.signal(signal.SIGALRM, signal.SIG_IGN)

        return container

    return wrapper
