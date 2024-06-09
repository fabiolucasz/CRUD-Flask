import os
from flask import Flask
from pacote.ext.appearance import Bootstrap
from pacote.ext.database import database_init_app
from pacote.ext.admin import init_app
from pacote.ext.routes import routes_init_app


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
database_init_app(app)
Bootstrap(app)
init_app(app)
routes_init_app(app)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
