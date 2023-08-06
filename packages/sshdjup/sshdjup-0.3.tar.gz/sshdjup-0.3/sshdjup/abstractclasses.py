from abc import ABC, abstractmethod


class ABCAnalizer(ABC):
    """ABC for main Analizer class,
    releases passed beneath methods.

    """
    
    @abstractmethod
    def get_ssh_data(self):
        """Should return namedtuple with cred data."""

        pass

    @abstractmethod
    def get_settings_dir(self):
        """Should return a string with settings dir."""

        pass

    @abstractmethod
    def get_static_dir(self):
        """Should return a string with static dir."""

        pass

    @abstractmethod
    def get_template_dir(self):
        """Should return a template dir."""

        pass

    @abstractmethod
    def get_db_dir(self):
        """Should return a database dir."""

        pass


