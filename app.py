from flask import Flask, render_template, request, redirect, url_for, flash
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cadastro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    escolaridade = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    anexo = db.Column(db.String(200), nullable=False)

# Criar a tabela
with app.app_context():
    db.create_all()

# Configurar Flask-Admin
class MyAdminIndexView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin.html')

admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=MyAdminIndexView(url='/admin'))

# Adicionar a visão de modelo padrão
admin.add_view(ModelView(Usuario, db.session))

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

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
