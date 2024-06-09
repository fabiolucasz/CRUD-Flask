from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def database_init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastro.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'
    db.init_app(app)
    with app.app_context():
        db.create_all()
