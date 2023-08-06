import os


def get_terminal_size():
    fallback = (80, 24)
    try:
        from shutil import get_terminal_size
    except ImportError:  # pragma: no cover
        try:
            import termios
            import fcntl
            import struct

            call = fcntl.ioctl(0, termios.TIOCGWINSZ, "\x00" * 8)
            height, width = struct.unpack("hhhh", call)[:2]
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            width = int(os.environ.get("COLUMNS", fallback[0]))
            height = int(os.environ.get("COLUMNS", fallback[1]))
        # Work around above returning width, height = 0, 0 in Emacs
        width = width if width != 0 else fallback[0]
        height = height if height != 0 else fallback[1]
        return width, height
    else:
        return get_terminal_size(fallback)
