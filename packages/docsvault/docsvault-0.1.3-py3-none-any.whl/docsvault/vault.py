"""
Define interface to implement in order to create Vault plugins.
"""
import abc
import os
import datetime
import aiofiles


class VaultABC(abc.ABC):
    """
    Abstract base class (interface) that should be implemented
    to create a DocsVault plugin.
    """

    @abc.abstractmethod
    def create_directory(self, _path):
        """
        Create given directory in the vault.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_directory(self, _path, _file):
        """
        Remove directory from the vault.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def browse_directory(self, _path):
        """
        Return content of the vault directory.
        """

    @abc.abstractmethod
    async def create_file(self, _path, _file):
        """
        Write ciphered file in the vault.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_file(self, _path, _file):
        """
        Delete ciphered file from the vault.
        """
        raise NotImplementedError


class LocalVault(VaultABC):
    """
    Plugin to interract with a local vault (local folder)
    """

    def __init__(self, _path):
        self.path = _path

    def _relative_to_vault_path(self, _path):
        return os.path.join(self.path, '' if _path is None else _path)

    def create_directory(self, _path):
        os.makedirs(self._relative_to_vault_path(_path))
        return {'success': True, 'message': 'Directory successfully created!'}

    def delete_directory(self, _path, _file):
        return NotImplemented

    def browse_directory(self, _path):
        real_path = self._relative_to_vault_path(_path)

        content = []

        for filename in os.listdir(real_path):
            content.append({
                'filename': filename,
                'relpath': os.path.join(_path, filename),
                'created': datetime.datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(real_path, filename))
                    ).strftime('%Y/%m/%d %H:%M:%S'),
                'filetype': 'folder' if os.path.isdir(os.path.join(real_path, filename)) else 'file'
            })

        return content

    async def create_file(self, _path, _file):
        directory = self._relative_to_vault_path(_path)

        async with aiofiles.open(os.path.join(directory, _file.name), 'wb') as file:
            await file.write(_file.body)

        return {'success': True, 'message': 'Stored in vault!'}

    def delete_file(self, _path, _file):
        return NotImplemented


if __name__ == '__main__':
    test_vault = LocalVault('vault')
    test_content = test_vault.browse_directory('credentials')
    print(test_content)
