import inspect
import logging
import time
from functools import wraps

log = logging.getLogger(__name__)


def timeit(*args, **kwargs):
    """A method decorator which can be applied on async and normal methods."""

    def _log_execution(start: float, name: str, coro, coro_args):
        total = time.time() - start
        if total >= 0.5:  # pragma: no cover
            log.warning(f'{name if name else coro.__name__} finished after %.3f seconds' % total)

    def inner(coro):
        @wraps(coro)
        async def wrapped(*coro_args, **coro_kwargs):
            name = kwargs.get('name')
            start = time.time()
            try:
                return await coro(*coro_args, **coro_kwargs)
            except Exception as e:
                raise e
            finally:
                _log_execution(start, name, coro, coro_args)

        @wraps(coro)
        def timed(*coro_args, **coro_kwargs):
            name = kwargs.get('name')
            start = time.time()

            try:
                return coro(*coro_args, **coro_kwargs)
            except Exception as e:
                raise e
            finally:
                _log_execution(start, name, coro, coro_args)

        if inspect.iscoroutinefunction(coro):
            return wrapped
        return timed

    if args:
        return inner(*args)
    else:
        return inner
