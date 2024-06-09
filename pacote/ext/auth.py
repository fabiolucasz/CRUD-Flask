from werkzeug.security import check_password_hash, generate_password_hash
from pacote.ext.database import db
from pacote.models import Adm

def verify_login(user):
    email = user.get('email')
    password = user.get('senha')
    if not email or not password:
        return False
    existing_user = Adm.query.filter_by(email=email).first()
    if not existing_user:
        return False
    if check_password_hash(existing_user.senha, password):
        return True
    return False

def create_user(nome, email, whatsapp, senha):
    if Adm.query.filter_by(email=email).first():
        raise RuntimeError(f'{email} já está cadastrado')
    user = Adm(nome=nome, email=email, whatsapp=whatsapp, senha=generate_password_hash(senha))
    db.session.add(user)
    db.session.commit()
    return user
