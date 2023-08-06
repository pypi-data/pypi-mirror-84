from .exceptions import (
    SSHFileExistingError,
    SSHCredentialsError,
    SettingsDirError,
    SettingsDirToError,
    ProjectDirError,
    ProjectDirToError,
    StaticDirError,
    StaticDirToError,
    TemplatesDirError,
    TemplatesDirToError,
    DbDirError,
    DbDirToError
)
from collections import namedtuple
from .abstractclasses import ABCAnalizer
import typing
import os


__all__ = ["Analizer"]


class MainAnalizer:
    """Main class for config file analizing
    it serves to get origin data, parce them
    and filter them afterwards.

    """

    available_params: tuple = (
        "HOST",
        "USERNAME",
        "PORT",
        "PASSWORD",
        "PROJECT_DIR",
        "PROJECT_DIR_TO", 
        "PROJECT_DB_DIR",
        "PROJECT_DB_DIR_TO",
        "PROJECT_SETTINGS_DIR",
        "PROJECT_SETTINGS_DIR_TO",
        "PROJECT_STATIC_DIR",
        "PROJECT_STATIC_DIR_TO",
        "PROJECT_TEMPLATES_DIR",
        "PROJECT_TEMPLATES_DIR_TO",
    )

    processed_data: dict = {}

    def _check_file_existing(self) -> bool:
        """Checks whether main config file 
        'SSHFile' exists.

        """

        return os.path.exists("SSHFile")

    def _get_origin_data(self) -> typing.List[str, ...]:
        """Gets original data from 'SSHFile'."""

        with open("SSHFile") as file:
            data = file.read().split("\n")
            del data[-1]
            return data

    def _get_processed_line(self, line: str) -> typing.Tuple[str, ...]:
        """Processes gotten text and returns tuple with two strings: param, value."""
    
        param, value = line.split("=")
        param = param.replace(" ", "").replace('"', '')
        value = value.replace(" ", "").replace('"', '')
        return (param.upper(), value)


    def _process_data(self, origin_data: typing.List[str, ...]) -> typing.Dict[str, typing.Union[str, int]]:
        """Processes origin data gotten from 'SSHFile'
        and returns made dictionary.

        """

        for line in origin_data:
            param, value = self._get_processed_line(line)
            if param in self.available_params:
                self.processed_data[param] = value 
        return self.processed_data

    def _parce_ssh_data(self) -> typing.NamedTuple:
        """Filters processed data and returns main
        credentials to connect via ssh.

        """
        
        ssh_data = namedtuple("SSHdata", ["host", "username", "port", "password"])
        return ssh_data(
            host=self.processed_data.get("HOST"),
            username=self.processed_data.get("USERNAME"),
            port=self.processed_data.get("PORT", 22),
            password=self.processed_data.get("PASSWORD")
        )

    def _analize_data(self) -> typing.Dict:
        """Main analizing method.
        Firstly checks whether config file exists,
        then, gets origin data and processes it.

        """

        if self._check_file_existing():
            origin_data = self._get_origin_data()
            self._process_data(origin_data)
            return self.processed_data
        raise SSHFileExistingError


class Analizer(MainAnalizer, ABCAnalizer):
    """Class imitates MainAnalizer.
    This property accepts to use main tools
    for the analization of the main config file.

    """


    def __init__(self):

        self.analized_data = self._analize_data()

    def _check_path_availability(self, method):
        """Runs method passed in the param and 
        that checks whether wanted path is written
        in the 'SSHFile'.

        """

        return getattr(self, method)()

    def get_ssh_data(self):
        """Returns all the important ssh data for the futher connection."""

        if data := self._parce_ssh_data():
            return data
        raise SSHCredentialsError

    def get_settings_dir(self):
        """Returns dir with settings file."""

        if path := self.analized_data.get("PROJECT_SETTINGS_DIR"):
            return path
        raise SettingsDirError

    def get_settings_dir_to(self):

        if path := self.analized_data.get("PROJECT_SETTINGS_DIR_TO"):
            return path
        raise SettingsDirToError

    def get_static_dir(self):
        """Returns dir with static folders and files."""

        if path := self.analized_data.get("PROJECT_STATIC_DIR"):
            return path
        raise StaticDirError

    def get_static_dir_to(self):
        """Returns path to dir where to save static files."""

        if path := self.analized_data.get("PROJECT_STATIC_DIR_TO"):
            return path
        raise StaticDirToError

    def get_template_dir(self):
        """Returns dir with templates folders."""

        if path := self.analized_data.get("PROJECT_TEMPLATES_DIR"):
            return path
        raise TemplatesDirError

    def get_template_dir_to(self):
        """Returns path to dir where should save files."""

        if path := self.analized_data.get("PROJECT_TEMPLATES_DIR_TO"):
            return path
        raise TemplatesDirToError

    def get_db_dir(self):
        """Returns dir with db files."""

        if path := self.analized_data.get("PROJECT_DB_DIR"):
            return path
        raise DbDirError

    def get_db_dir_to(self):
        """Returns dir where should save files."""

        if path := self.analized_data.get("PROJECT_DB_DIR_TO"):
            return path
        raise DbDirToError

    def get_project_dir(self):
        """Returns main project dir."""

        if path := self.analized_data.get("PROJECT_DIR"):
            return path
        raise ProjectDirError

    def get_project_dir_to(self):
        """Returns dir where should save files."""

        if path := self.analized_data.get("PROJECT_DIR_TO"):
            return path
        raise ProjectDirToError
