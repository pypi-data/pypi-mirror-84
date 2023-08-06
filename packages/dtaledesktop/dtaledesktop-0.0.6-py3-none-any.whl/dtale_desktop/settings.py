"""
Environment variables that can be used to configure settings:
- DTALEDESKTOP_HOST
- DTALEDESKTOP_PORT
- DTALEDESKTOP_DTALE_PORT
- DTALEDESKTOP_ROOT_DIR:
    path, the location where all persistent data (loaders, cached data, etc.) will be stored.
    By default this is ~/.dtaledesktop
- DTALEDESKTOP_ADDITIONAL_LOADERS_DIRS:
    comma-separated list of directory paths that should be scanned for data sources upon startup.
- DTALEDESKTOP_DISABLE_ADD_DATA_SOURCES:
    "true" if the "Add Data Source" button should not be shown.
- DTALEDESKTOP_DISABLE_EDIT_DATA_SOURCES:
    "true" if editing existing data sources should not be allowed.
- DTALEDESKTOP_DISABLE_EDIT_LAYOUT:
    "true" if users should not be allowed to edit what sources are/are not visible or what order they're in.
- DTALEDESKTOP_DISABLE_PROFILE_REPORTS:
    "true" if the "Profile" option (which builds a pandas_profiling report) should not be shown.
    This is resource-intensive and currently a bit buggy (it launches a subprocess).
"""
import os
import socket
from typing import List, Optional

from dtale_desktop.pydantic_utils import BaseApiModel

__all__ = ["settings"]

_SENTINEL = object()


class _Settings:
    ROOT_DIR: str
    ADDITIONAL_LOADERS_DIRS: List[str]
    DISABLE_ADD_DATA_SOURCES: bool
    DISABLE_EDIT_DATA_SOURCES: bool
    DISABLE_EDIT_LAYOUT: bool
    DISABLE_PROFILE_REPORTS: bool
    HOST: str
    PORT: int
    DTALE_PORT: Optional[int]

    _instance = _SENTINEL

    def __init__(self):
        if self._instance is not _SENTINEL:
            raise Exception("_Settings is a singleton")
        self._instance = self

        self._HOST = os.getenv("DTALEDESKTOP_HOST", None)

        try:
            self._PORT = int(os.getenv("DTALEDESKTOP_PORT"))
        except (ValueError, TypeError):
            self._PORT = None

        try:
            self.DTALE_PORT = int(os.getenv("DTALEDESKTOP_DTALE_PORT"))
        except (ValueError, TypeError):
            self.DTALE_PORT = None

        self.ROOT_DIR = os.getenv(
            "DTALEDESKTOP_ROOT_DIR",
            os.path.join(os.path.expanduser("~"), ".dtaledesktop"),
        )
        self.ADDITIONAL_LOADERS_DIRS = [
            x
            for x in os.getenv("DTALEDESKTOP_ADDITIONAL_LOADERS_DIRS", "").split(",")
            if x != ""
        ]
        self.DISABLE_ADD_DATA_SOURCES = (
            os.getenv("DTALEDESKTOP_DISABLE_ADD_DATA_SOURCES", "").lower() == "true"
        )
        self.DISABLE_EDIT_DATA_SOURCES = (
            os.getenv("DTALEDESKTOP_DISABLE_EDIT_DATA_SOURCES", "").lower() == "true"
        )
        self.DISABLE_EDIT_LAYOUT = (
            os.getenv("DTALEDESKTOP_DISABLE_EDIT_LAYOUT", "").lower() == "true"
        )
        self.DISABLE_PROFILE_REPORTS = (
            os.getenv("DTALEDESKTOP_DISABLE_PROFILE_REPORTS", "").lower() == "true"
        )

    @property
    def HOST(self) -> str:
        if self._HOST is None:
            try:
                self._HOST = socket.gethostbyname("localhost")
            except BaseException:
                self._HOST = socket.gethostbyname(socket.gethostname())
        return self._HOST

    @property
    def PORT(self) -> int:
        if self._PORT is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("", 0))
            self._PORT = sock.getsockname()[1]
            sock.close()
        return self._PORT

    class Serialized(BaseApiModel):
        disable_add_data_sources: bool
        disable_edit_data_sources: bool
        disable_edit_layout: bool
        disable_profile_reports: bool

    def serialize(self) -> Serialized:
        return self.Serialized(
            disable_add_data_sources=self.DISABLE_ADD_DATA_SOURCES,
            disable_edit_data_sources=self.DISABLE_EDIT_DATA_SOURCES,
            disable_edit_layout=self.DISABLE_EDIT_LAYOUT,
            disable_profile_reports=self.DISABLE_PROFILE_REPORTS,
        )


settings = _Settings()
