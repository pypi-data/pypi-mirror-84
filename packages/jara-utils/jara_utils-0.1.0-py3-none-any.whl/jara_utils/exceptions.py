class JaraError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class EnvironmentVariableNotFound(JaraError):
    """Raise this exception when an environment variable is not defined, but should be."""
    def __init__(self, variable_name: str):
        super().__init__(f'Environment variable with name {variable_name} not found!')
