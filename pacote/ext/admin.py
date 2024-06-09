from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from pacote.ext.database import db
from pacote.models import Usuario, Adm

admin = Admin()


def init_app(app):
    admin.template_mode = "bootstrap3"
    admin.init_app(app)
    admin.add_view(ModelView(Usuario, db.session))
    admin.add_view(ModelView(Adm, db.session))

