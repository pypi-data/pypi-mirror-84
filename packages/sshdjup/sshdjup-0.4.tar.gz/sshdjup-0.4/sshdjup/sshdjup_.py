from .analizer import Analizer
from .settings import start_ssh_connection 
from .extensions import Commands


def start_updating():
    """Starts main exutable process of updating files."""

    analizer = Analizer()
    ssh_data = analizer.get_ssh_data()
    ssh_client = start_ssh_connection(
        ssh_data.host,
        ssh_data.username,
        ssh_data.port,
        ssh_data.password
    )
    commands = Commands(ssh_client)
    commands.main_command_loop()

    


if __name__ == "__main__":
    start_updating()