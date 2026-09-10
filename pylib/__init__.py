def range(start, stop, step):
    if step <= 0:
        raise ValueError
    if start > stop:
        while start >= stop:
            yield start
            start -= step
    elif start < stop:
        while start <= stop:
            yield start
            start += step
    else:
        raise ValueError
builtins_all = all
def all(*args):
    if len(args) == 1:
        return builtins_all(args[0])
    return builtins_all(args)
builtins_any = any
def any(*args):
    if len(args) == 1:
        return builtins_any(args[0])
    return builtins_any(args)
builtins_sum = sum
def sum(*args):
    if len(args) == 1:
        return builtins_sum(args[0])
    return builtins_sum(args)