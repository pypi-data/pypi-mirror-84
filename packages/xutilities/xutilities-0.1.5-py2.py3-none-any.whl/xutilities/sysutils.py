# -*- coding: utf-8 -*-

"""System utilities."""

import os
import sys
from pathlib import Path


class ExecutableNotFoundException(Exception):
    """Given executable not found in path."""

    def __init__(self, executable: str):
        super().__init__(f"Executable not found in path: {executable}")
        self.executable = executable


class NoVirtualEnvironmentException(Exception):
    """No virtual environment detected."""

    def __init__(
        self, path: Path = None, markers: [Path] = None, caused_by: Exception = None
    ):
        super().__init__()
        self.path = path
        self.markers = markers
        self.caused_by = caused_by
        self.msg = str(self)

    def __str__(self):
        msgs = []
        if self.path is not None:
            msgs.append(f"path={str(self.path)}")
        if self.markers is not None:
            msgs.append(
                f"markers= " f"{', '.join([str(marker) for marker in self.markers])}"
            )
        if self.caused_by is not None:
            msgs.append(str(self.caused_by))
        if len(msgs) == 0:
            msgs.append("No arguments given.")
        return ", ".join(msgs)


def which(executable: str) -> Path:
    """Looks in $PATH for `executable`.

    :param executable: name of executable to look up.
    :type executable: str
    :return: absolute path of executable.
    :rtype: pathlib.Path
    :raises ExecutableNotFoundException: if executable not found in path.
    """
    for exec_path in os.get_exec_path():
        path = Path(exec_path) / executable
        if path.exists():
            return path.absolute()
    raise ExecutableNotFoundException(executable)


def get_venv() -> Path:
    """Determine path to active virtual environment.

    :return: path to virtual environment.
    :rtype: pathlib.Path
    :raises ExecutableNotFoundException: if python not found in path.
    :raises NoVirtualEnvironmentException: if no virtual environment was found.
    """
    try:
        path = which("python").parent.parent
    except ExecutableNotFoundException as e:
        tb = sys.exc_info()[2]
        raise NoVirtualEnvironmentException(caused_by=e).with_traceback(tb)
    venv_markers = [path / "pyvenv.cfg", path / "conda-meta"]
    if (
        not any([marker.exists() for marker in venv_markers])
        and "virtualenv" not in path.parts  # e.g. for travis
    ):
        raise NoVirtualEnvironmentException(path=path, markers=venv_markers)
    return path
