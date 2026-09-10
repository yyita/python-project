import time
import itertools
import functools
import unitlib
def _time_cost(
    call,
    times = 1,
    unit = "s"
):
    t1 = time.perf_counter_ns()
    for _ in itertools.repeat(None, int(times)):
        call()
    t2 = time.perf_counter_ns()
    return unitlib.convert(t2 - t1, "ns", unit)
def time_cost(
    call = None,
    times = 1,
    unit = "s"
):
    if call is None:
        def decorator(call):
            @functools.wraps(call)
            def wrapper():
                return _time_cost(call, times, unit)
            return wrapper
        return decorator
    return _time_cost(call, times, unit)
def _per_times(
    call,
    times = 1,
    unit = "s"
):
    cost = time_cost(call, times, unit)
    return cost / times
def per_times(
    call = None,
    times = 1,
    unit = "s"
):
    if call is None:
        def decorator(call):
            @functools.wraps(call)
            def wrapper():
                return _per_times(call, times, unit)
            return wrapper
        return decorator
    return _per_times(call, times, unit)
def _times_per(
    call,
    times = 1,
    unit = "s"
):
    cost = time_cost(call, times, unit)
    try:
        return times / cost
    except ZeroDivisionError:
        return float("inf")
def times_per(
    call = None,
    times = 1,
    unit = "s"
):
    if call is None:
        def decorator(call):
            @functools.wraps(call)
            def wrapper():
                return _times_per(call, times, unit)
            return wrapper
        return decorator
    return _times_per(call, times, unit)