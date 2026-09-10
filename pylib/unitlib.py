from enum import Enum as _Enum
class DataUnit(_Enum):
    b = 0.125
    B  = 1
    KB = 1000
    MB = 1000 ** 2
    GB = 1000 ** 3
    TB = 1000 ** 4
    PB = 1000 ** 5
    EB = 1000 ** 6
    ZB = 1000 ** 7
    YB = 1000 ** 8
    KiB = 1 << 10
    MiB = 1 << 20
    GiB = 1 << 30
    TiB = 1 << 40
    PiB = 1 << 50
    EiB = 1 << 60
    ZiB = 1 << 70
    YiB = 1 << 80
    Kb = 125
    Mb = 125 * 1000
    Gb = 125 * 1000 ** 2
    Tb = 125 * 1000 ** 3
    Pb = 125 * 1000 ** 4
    Eb = 125 * 1000 ** 5
    Zb = 125 * 1000 ** 6
    Yb = 125 * 1000 ** 7
    Kib = 128
    Mib = 128 << 10
    Gib = 128 << 20
    Tib = 128 << 30
    Pib = 128 << 40
    Eib = 128 << 50
    Zib = 128 << 60
    Yib = 128 << 70
class TimeUnit(_Enum):
    ps = 1e-12
    ns = 1e-9
    us = 1e-6
    ms = 1e-3
    s = 1
    m = 60
    h = 3600
    d = 86400
    w = 604800
    y = 31557600
def convert(
    real_number: int | float,
    unit_from: _Enum,
    unit_to: _Enum
):  return real_number * unit_from.value / unit_to.value