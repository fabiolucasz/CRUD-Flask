import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
admin = Admin()
Bootstrap(app)


# Modelo de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    escolaridade = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    anexo = db.Column(db.String(200), nullable=False)
    posts = db.relationship("Post", back_populates="user")

    def __str__(self):
        return self.nome


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    user = db.relationship("Usuario", back_populates="posts")

class PostView(ModelView):
    can_delete = False
    form_columns = ["title", "body", "user"]
    column_list = ["title", "body", "user"]


#exportar banco de dados como .xlsx
def converter_para_excel():
    # Configurar a conexão com o banco de dados
    engine = create_engine('sqlite:///instance/db.sqlite3')

    # Consultar os dados da tabela User e salvar em um DataFrame do Pandas
    df = pd.read_sql_table('User', engine)

    # Salvar o DataFrame em um arquivo Excel
    df.to_excel('usuarios.xlsx', index=False)


# Configurando o Flask-Admin
admin.init_app(app)
admin.add_view(ModelView(Usuario, db.session))
admin.add_view(PostView(Post, db.session))

# Criar a tabela
with app.app_context():
    db.create_all()


# Página inicial
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Adicione sua lógica de login aqui
        pass
    return render_template('login.html')


@app.route('/admin/')
def admin_panel():
    # Aqui você pode adicionar lógica para verificar se o usuário está logado como admin
    # e, em caso afirmativo, fornecer acesso à página admin
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

            # Insira aqui o código para inserir os dados na tabela 'usuarios'
            novo_usuario = Usuario(nome=nome, idade=idade, email=email, escolaridade=escolaridade, whatsapp=whatsapp, anexo=anexo_path)
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
