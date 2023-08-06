

class SSHFileExistingError(Exception):

    def __str__(self):
        return "'SSHFile' doesnt't exist in this directory."


class SettingsDirError(Exception):

    def __str__(self):
        return "SettingsDir hasn't been passed"


class SettingsDirToError(Exception):

    def __str__(self):
        return "SettingsDirTo hasn't been passed"


class SSHCredentialsError(Exception):

    def __str__(self):
        return "You have't passed important ssh credentials like 'host', 'username', 'port'(optional), 'password'"


class ProjectDirError(Exception):
    
    def __str__(self):
        return "You haven't passed 'PROJECT_DIR' variable in SSHFile"


class ProjectDirToError(Exception):
    
    def __str__(self):
        return "You haven't passed 'PROJECT_DIR_TO' variable in SSHFile"


class StaticDirError(Exception):

    def __str__(self):
        return "You haven't passed 'STATIC_DIR' variable in SSHFile"


class StaticDirToError(Exception):

    def __str__(self):
        return "You haven't passed 'STATIC_DIR_TO' variable in SSHFile"


class TemplatesDirError(Exception):

    def __str__(self):
        return "You haven't passed 'PROJECT_TEMPLATES_DIR' variable in SSHFile"


class TemplatesDirToError(Exception):

    def __str__(self):
        return "You haven't passed 'PROJECT_TEMPLATES_DIR_TO' variable in SSHFile"


class DbDirError(Exception):

    def __str__(self):
        return "You haven't passed 'PROJECT_DB_DIR' variable in SSHFile"

class DbDirToError(Exception):

    def __str__(self):
        return "You haven't passed 'PROJECT_DB_DIR_TO' variable in SSHFile"