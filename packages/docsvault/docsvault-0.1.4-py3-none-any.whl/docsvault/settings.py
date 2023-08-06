"""
Middleware object used to abstract interractions with a
local settings file for docsvault.
"""
import uuid

UNDEFINED = uuid.uuid4()


class Settings:
    """
    Object used to interract with local settings file.
    """

    def __init__(self):
        """
        Load settings from local settings file
        """
        self.settings = {
            'local_vault': 'vault',
            'remote_vault': None
        }

    def get(self, key: str, default=UNDEFINED):
        """
        Extract value from the configuration file.

        Positional arguments:
            key -- (str) Path of the key in json notation
            default -- (any) Value to return if key is not found in settings

        Raises:
            KeyEror -- If value is not found and default value is not provided
        """
        value = self.settings.get(key, default)

        if value is UNDEFINED:
            raise KeyError('{} not found in settings'.format(key))

        return value

    def set(self, key: str, value: object):
        """
        Edit value of a setting.
        """


settings = Settings()
