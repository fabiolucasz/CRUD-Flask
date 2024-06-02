import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
admin = Admin(app)
Bootstrap(app)

class Adm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    whatsapp = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.nome

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    escolaridade = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    anexo = db.Column(db.String(200), nullable=False)

    def __str__(self):
        return self.nome

# Configurando o Flask-Admin
admin.add_view(ModelView(Usuario, db.session))
admin.add_view(ModelView(Adm, db.session))

# Exportar banco de dados como .xlsx
def converter_para_excel():
    engine = create_engine('sqlite:///cadastro.db')
    df = pd.read_sql_table('usuario', engine)
    df.to_excel('usuarios.xlsx', index=False)

# Criar a tabela
with app.app_context():
    db.create_all()

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de registro
@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    admin_user = Adm.query.filter_by(email=email, senha=password).first()

    if admin_user:
        session['logged_in'] = True
        session['admin_user_id'] = admin_user.id
        return redirect(url_for('admin_panel'))
    else:
        flash('Email ou senha inválidos.')
        return redirect(url_for('index'))

@app.route('/admin/')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('admin_panel.html')

# Rota para lidar com o registro de usuários
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        email = request.form['email']
        escolaridade = request.form['escolaridade']
        whatsapp = request.form['whatsapp']
        anexo = request.files['anexo']

        if anexo and anexo.filename.endswith('.pdf'):
            anexo_filename = f"{nome}_{anexo.filename}"
            anexo_path = os.path.join(app.config['UPLOAD_FOLDER'], anexo_filename)
            anexo.save(anexo_path)

            novo_usuario = Usuario(
                nome=nome,
                idade=idade,
                email=email,
                escolaridade=escolaridade,
                whatsapp=whatsapp,
                anexo=anexo_path
            )
            db.session.add(novo_usuario)
            db.session.commit()

            flash('Usuário registrado com sucesso!')
            return redirect(url_for('index'))
        else:
            flash('Por favor, envie um arquivo PDF.')
            return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
