# The MIT License (MIT)

# Copyright (c) 2013-2022 Damien P. George

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# --------------------------------------------------------------------------------

# Unless specified otherwise (see below), the above license and copyright applies
# to all files in this repository.

# Individual files may include additional copyright holders.

# The various ports of MicroPython may include third-party software that is
# licensed under different terms. These licenses are summarised in the tree
# below, please refer to these files and directories for further license and
# copyright information. Note that (L)GPL-licensed code listed below is only
# used during the build process and is not part of the compiled source code.

# / (MIT)
#     /drivers
#         /cc3000 (BSD-3-clause)
#         /cc3100 (BSD-3-clause)
#         /wiznet5k (BSD-3-clause)
#     /lib
#         /asf4 (Apache-2.0)
#         /axtls (BSD-3-clause)
#             /config
#                 /scripts
#                     /config (GPL-2.0-or-later)
#                 /Rules.mak (GPL-2.0)
#         /berkeley-db-1xx (BSD-4-clause)
#         /btstack (See btstack/LICENSE)
#         /cmsis (BSD-3-clause)
#         /crypto-algorithms (NONE)
#         /libhydrogen (ISC)
#         /littlefs (BSD-3-clause)
#         /lwip (BSD-3-clause)
#         /mynewt-nimble (Apache-2.0)
#         /nrfx (BSD-3-clause)
#         /nxp_driver (BSD-3-Clause)
#         /oofatfs (BSD-1-clause)
#         /pico-sdk (BSD-3-clause)
#         /re15 (BSD-3-clause)
#         /stm32lib (BSD-3-clause)
#         /tinytest (BSD-3-clause)
#         /tinyusb (MIT)
#         /uzlib (Zlib)
#     /logo (uses OFL-1.1)
#     /ports
#         /cc3200
#             /hal (BSD-3-clause)
#             /simplelink (BSD-3-clause)
#             /FreeRTOS (GPL-2.0 with FreeRTOS exception)
#         /stm32
#             /usbd*.c (MCD-ST Liberty SW License Agreement V2)
#             /stm32_it.* (MIT + BSD-3-clause)
#             /system_stm32*.c (MIT + BSD-3-clause)
#             /boards
#                 /startup_stm32*.s (BSD-3-clause)
#                 /*/stm32*.h (BSD-3-clause)
#             /usbdev (MCD-ST Liberty SW License Agreement V2)
#             /usbhost (MCD-ST Liberty SW License Agreement V2)
#         /teensy
#             /core (PJRC.COM)
#         /zephyr
#             /src (Apache-2.0)
#     /tools
#         /dfu.py (LGPL-3.0-only)

try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

from machine import RTC
from utime import gmtime

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
__NTP_DELTA = 3155673600

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
__HOST = "time.google.com"


def __time(host):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - __NTP_DELTA


# There's currently no timezone support in MicroPython, and the RTC is set in UTC time.
def settime(timezone: int = 2, host: str = __HOST):
    t = __time(host)
    

    tm = gmtime(t)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3] + timezone, tm[4], tm[5], 0))