"""
Define groups of routes to serve static content.
"""
import os
from sanic import Blueprint


webui = Blueprint('webui')

DOCSVAULT_PATH = os.path.dirname(os.path.realpath(__file__))
FRONTEND_PATH = os.path.join(DOCSVAULT_PATH, 'static')

webui.static('/', FRONTEND_PATH + '/index.html')
webui.static('/favicon.ico', FRONTEND_PATH + '/favicon.ico')

webui.static('/css', FRONTEND_PATH + '/css')
webui.static('/img', FRONTEND_PATH + '/img')
webui.static('/js', FRONTEND_PATH + '/js')
