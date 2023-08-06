"""
Create sanic ASGI web application that is launched in debug
mode if this script is called directly.
"""
from sanic import Sanic
from sanic_cors import CORS

from .webui import webui
from .api import api

app = Sanic()
CORS(app)

app.register_blueprint(webui)
app.register_blueprint(api, url_prefix='/api')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
