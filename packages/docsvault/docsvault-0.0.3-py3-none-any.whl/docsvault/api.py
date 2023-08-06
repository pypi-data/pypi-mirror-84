"""
Define endpoints for docsvault's API.
"""
from sanic import response, Blueprint

from .settings import settings
from .vault import LocalVault


api = Blueprint('api')
vault = LocalVault(settings.get('local_vault'))


@api.get('/browse')
@api.get('/browse/<_path:path>')
async def api_browse_vault(_request, _path=''):
    """
    Return content of given directory
    """
    result = vault.browse_directory(_path)
    return response.json(result)


@api.post('/vault/upload')
@api.post('/vault/upload/<_path:path>')
async def upload_file(request, _path=None):
    """
    Send file and upload it to the vault
    """
    result = await vault.create_file(_path, request.files["file"][0])
    return response.json(result)


@api.post('/vault/directory/<_path:path>')
async def create_directory(_request, _path):
    """
    Create a new directory in the vault
    """
    result = vault.create_directory(_path)
    return response.json(result)
