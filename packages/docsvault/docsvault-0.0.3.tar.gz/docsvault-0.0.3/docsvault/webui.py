"""
Define groups of routes to serve static content.
"""
from sanic import Blueprint


webui = Blueprint('webui')

FRONTEND_PATH = 'docsvault/static'

webui.static('/', FRONTEND_PATH + '/index.html')
webui.static('/favicon.ico', FRONTEND_PATH + '/favicon.ico')

webui.static('/css', FRONTEND_PATH + '/css')
webui.static('/img', FRONTEND_PATH + '/img')
webui.static('/js', FRONTEND_PATH + '/js')
