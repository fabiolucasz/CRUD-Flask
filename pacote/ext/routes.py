import os
from flask import render_template, request, redirect, url_for, flash, session, g
from pacote.ext.auth import create_user
from pacote.ext.database import db
from pacote.models import Adm, Usuario
from werkzeug.security import check_password_hash


def routes_init_app(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            session.pop('user', None)
            if request.form['password'] == 'password':
                session['user'] = request.form['username']
                return redirect(url_for('protected'))
        return render_template('index.html')

    @app.route('/candidato', methods=['POST'])
    def novo_candidato():
        if request.method == 'POST':
            # Capturando os dados do formulário
            nome = request.form['nome']
            idade = request.form['idade']
            email = request.form['email']
            escolaridade = request.form['escolaridade']
            whatsapp = request.form['whatsapp']
            anexo = request.files['anexo']

            # Salvando o arquivo na pasta local
            pasta_destino = 'uploads'  # Pasta onde os arquivos serão salvos
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)

            caminho_arquivo = os.path.join(pasta_destino, anexo.filename)
            anexo.save(caminho_arquivo)

            # Criando uma nova instância de User e inserindo no banco de dados
            novo_candidato = Usuario(nome=nome, idade=idade, email=email, escolaridade=escolaridade, whatsapp=whatsapp,
                                anexo=caminho_arquivo)
            db.session.add(novo_candidato)
            db.session.commit()
            return "Dados cadastrados com sucesso!"
        return render_template("novo_candidato.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session.pop('user', None)  # Limpa a sessão ao tentar fazer login

            email = request.form['email']
            password = request.form['password']

            user = Adm.query.filter_by(email=email).first()

            if user and check_password_hash(user.senha, password):
                session['user'] = user.email
                return redirect(url_for('protected'))
            else:
                flash('Credenciais inválidas, tente novamente.')

        return render_template('login_adm.html')

    @app.route('/admin/')
    def admin():
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return render_template('admin.html', user=session['user'])

    @app.route('/novoadm', methods=['GET', 'POST'])
    def novo_adm():
        if not session.get('logged_in'):
            return redirect(url_for('login'))

        if request.method == 'POST':
            nome = request.form['name']
            email = request.form['email']
            whatsapp = request.form['whatsapp']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash('As senhas não coincidem!')
                return redirect(url_for('novo_adm'))

            try:
                create_user(nome, email, whatsapp, password)
                flash('Usuário registrado com sucesso!')
                return redirect(url_for('admin'))
            except RuntimeError as e:
                flash(str(e))
                return redirect(url_for('novo_adm'))

        return render_template('novo_adm.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logout realizado com sucesso')
        return redirect(url_for('index'))

    @app.route('/protected')
    def protected():
        if g.user:
            return render_template('protected.html', user=session['user'])
        return redirect(url_for('index'))

    # Executado antes de cada solicitação, verifica se o usuário está na sessão
    @app.before_request
    def before_request():
        g.user = session.get('user')
        if 'user' not in session and request.endpoint in ['protected']:
            return redirect(url_for('index'))
