import os
import sys
import typing
import scp
import paramiko
from .settings import SSHConnector


class MainDeleter:
    """MainDeleter serves to give utilible methods
    to help delete process, namely:
    - '_delete_old_iter': deletes files using passed values using cycle,
    - '_delete_old': deletes file passed in param,
    - '_get_errors': returns gotten errors happened during files deleting.
    
    """

    def _delete_old_iter(self, values: typing.List[str, ...]) -> typing.Union[list, None]:
        """Deletes files passed in the list using cycle."""

        errors = []
        for value in values:
            _, _, stderr = self.SSH.exec_command(f"rm -r {os.path.join(self.destdel_path, value)}")
            if stderr.read().decode():
                errors.append({value: stderr.read().decode()})
        return errors

    def _delete_old(self, value: typing.Union[str, None]) -> typing.Union[typing.List[str, ...], None]:
        """Deletes file passed in value."""

        errors = []
        del_path = os.path.join(self.destdel_path, value) if value else self.destdel_path
        _, _, stderr = self.SSH.exec_command(f"rm -r {del_path}")
        if stderr.read().decode():
            errors.append(stderr.read().decode())
        return errors

    @staticmethod
    def _get_errors(result: typing.Union[typing.List[str, ...], None]) -> None:
        if result:
            for error in result:
                sys.stdout.write(error)


class Deleter(MainDeleter):
    """Deleter class serves the abstract method above 'MainDeleter'.
    Uses 'delete_old' method to communicate with util methods in super class.

    """

    def delete_old(self, values: typing.Union[typing.List[str, ...], str]):
        """Deletes all the old files passed to delete in param"""

        if isinstance(values, list):
            result = self._delete_old_iter(values)
        else:
            result = self._delete_old(values)
        self._get_errors(result)


class MainUpdater(Deleter):
    """Class setves to give some additional methods like:
    - '_update_iter': updates files passed in 'value' param using cycle,
    - '_update_single': updates file passed in 'value' param,

    """

    def _update_iter(self, values: typing.List[str, ...]) -> bool:
        """Updates all the files passed in 'values' list."""

        for value in values:
            self.scp_client.put(
                os.path.join(self.files_path, value),
                recursive=True,
                remote_path=os.path.join(self.destdel_path, value)
            )
        return True


    def _update_single(self, value: typing.Union[str, None]) -> bool:
        """Updates single file passed in 'value' param."""

        dest_path = os.path.join(self.destdel_path, value) if value else self.destdel_path
        file_path = os.path.join(self.files_path, value) if value else self.files_path
        self.scp_client.put(
            file_path,
            recursive=True,
            remote_path=dest_path
        )
        return True


    def get_path_without_app_name(self):
        pass

    def get_path_with_app_name(self):
        pass


class Updater(MainUpdater):
    """Main class to use updation system
    allows user to update data.

    """

    def __init__(self, ssh_client: paramiko.SSHClient):

        self.SSH = ssh_client

    def update_files(self, from_path: str, to_path: str, value: typing.Union[typing.List[str, ...], str]) -> bool:
        """Updates files using passed params:
        - 'from_path' used to get files from the equal directory
          for the futher updating
        - 'to_path' used to get path where to save new files
        - 'value' contains values important to update
          can be both 'str' and 'list' with str objects in it.

        """
        
        self.destdel_path = to_path
        self.delete_old(value)
        self.files_path = from_path
        with scp.SCPClient(self.SSH.get_transport()) as self.scp_client:
            if isinstance(value, list):
                return self._update_iter(value)
            return self._update_single(value)