import os
import io

from GLXShell.libs.utils.id import new_id


def get_os_temporary_dir():
    """
    Get the OS default dir , the better as it can.

    It suppose to be cross platform

    :return: A tmp dir path
    :rtype: str
    """
    text_flags = os.O_RDWR | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        text_flags |= os.O_NOFOLLOW

    bin_flags = text_flags
    if hasattr(os, "O_BINARY"):  # pragma: no cover
        bin_flags |= os.O_BINARY

    directory_list = list()

    # First, try the environment.
    for envname in "TMPDIR", "TEMP", "TMP":
        dirname = os.getenv(envname)
        if dirname:
            directory_list.append(os.path.abspath(dirname))

    directory_list.extend(["/tmp", "/var/tmp", "/usr/tmp"])

    for directory in directory_list:
        if directory != os.path.curdir:
            directory = os.path.abspath(directory)

        name = str("glxshell-")
        name += str(new_id())
        name += str(".cp")
        filename = os.path.join(directory, name)
        try:
            fd = os.open(filename, bin_flags, 0o600)
            try:
                try:
                    with io.open(fd, "wb", closefd=False) as fp:
                        fp.write(b"Test")
                finally:
                    os.close(fd)
            finally:
                os.unlink(filename)
            return directory

        except PermissionError:  # pragma: no cover
            break  # no point trying more names in this directory
        except OSError:  # pragma: no cover
            break  # no point trying more names in this directory
    raise FileNotFoundError(  # pragma: no cover
        "No usable temporary directory found in %s" % directory_list
    )
