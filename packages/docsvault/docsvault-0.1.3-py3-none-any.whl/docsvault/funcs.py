"""
Deprecated, will be deleted in profit of an implementation of
a LocalVault class that implement VaultABC.
"""
import os
from datetime import datetime
from .settings import settings


def browse_vault(rel_path=''):
    """
    Retrieve vault content of given directory
    """
    content = []

    if not rel_path:
        real_path = settings.get('local_vault')
    else:
        real_path = os.path.join(settings.get('local_vault'), rel_path)

    for filename in os.listdir(real_path):

        content.append({
            'filename': filename,
            'relpath': os.path.join(rel_path, filename),
            'created': datetime.fromtimestamp(
                os.path.getmtime(os.path.join(real_path, filename))).strftime('%Y/%m/%d %H:%M:%S'),
            'filetype': 'folder' if os.path.isdir(os.path.join(real_path, filename)) else 'file'
        })

    return content
