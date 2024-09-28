from flask import Flask, url_for, render_template, request, jsonify, redirect, session
import db
from db import validar_email, validar_senha, verificar_login, validar_nome, validar_nome_contato, validar_email_contato, validar_mensagem_contato



import mysql.connector



app = Flask(__name__)
app.secret_key = 'chave_secreta' #chave secreta aqui



@app.route('/')
def index_cadastro():
    return render_template('cadastro.html')



@app.route('/create_table', methods=['POST'])
def create_tables():
    db.create_tables()
    return f"messagem : tabelas criadas com sucesso"



@app.route('/add_usuario', methods=['GET', 'POST'])
def add_usuario():
    # fazer o select
    if request.method == 'POST':
        nome = request.form['name']
        email = request.form['email']
        senha = request.form['password']
        data_nascimento = request.form['data-nascimento']

        usuario_adcionado = db.add_usuario(nome, email, senha, data_nascimento)

        #validar antes de enserir no banco de dados
        if not db.validar_nome(nome):
            return render_template('cadastro.html', error='O nome deve conter apenas letras ou espacos')

        if not db.validar_email(email):
            return render_template('cadastro.html', error='Email invalido')
        

        if not db.validar_senha(senha):
            return render_template('cadastro.html', error='Senha deve ter no minimo 6 caracteres!')

        #verificar se o email ja existe
        if not usuario_adcionado:
            return render_template('cadastro.html', error='Email ja cadastrado. Use outro email')
        

        return redirect(url_for('login'))
    
    return f"nome = {nome}, email = {email}, data nascimento = {data_nascimento}"



@app.route('/usuarios', methods=['GET'])
def get_usuario():
    usuario = db.get_usuario()
    return jsonify(usuario)

#Adcionar evento 


@app.route('/add_evento', methods=['POST'])
def add_evento():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao_evento = request.form['descricao_evento']
        data_evento = request.form['data_evento']
        id_usuario = request.form['id_usuario']

        db.add_evento(titulo, descricao_evento, data_evento, id_usuario)
    return jsonify({"message" : "Evento adcionado com sucesso!"})



@app.route('/eventos', methods=['GET'])
def get_eventos():
    eventos = db.get_evento
    return jsonify(eventos)



@app.route('/login.html', methods=['GET', 'POST'])
def login():

    # fazer o select
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']

        user = db.verificar_login(email, senha)

        # salva o id do usuario permitindo que ele so entre na rota home se estiver cadastrado
        if user:
            session['user_id'] = user[0]['id']
            return render_template('home.html')
        else:
            return render_template('login.html', error='Email ou senha incorretos!')
        
    return render_template('login.html')



@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/contato.html', methods=['POST', 'GET'])
def contato():
    if request.method == 'POST':
        name_contato = request.form['name_contato']
        email_contato = request.form['email_contato']
        mensagem_contato = request.form['mensagem_contato']

        contato_adcionado = db.add_contato(name_contato, email_contato, mensagem_contato)
        
        # validar antes de inserir no Banco de Dados

        if not db.validar_nome_contato(name_contato):
            return render_template('contato.html', error='Nome invalido !')

        if not db.validar_email_contato(email_contato):
            return render_template('contato.html', error='Email invalido !')


        if not db.validar_mensagem_contato(mensagem_contato):
            return render_template('contato.html', error='Mensagem muito curta ou muito longa')


        if not contato_adcionado:
            return render_template('contato.html', error='Email ja cadastrado !')




    return render_template('contato.html')






app.run(debug=True)