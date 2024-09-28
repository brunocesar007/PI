

#####################################################

import mysql.connector
import re


# Conexão com o banco de dados (mudar se necessario)
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="46011031aA@",
        database="pi"
    )
    return conn


####################################################

# Criando as tabelas
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nome VARCHAR(100),
        email VARCHAR(100),
        senha VARCHAR(45),
        data_nascimento DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evento (
        id INT PRIMARY KEY AUTO_INCREMENT,
        titulo VARCHAR(100),
        descricao_evento VARCHAR(150),
        data_evento DATE,
        id_usuario INT,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contato
    id INT PRIMARY KEY AUTO_INCREMENTE,
    name_contato VARCHAR(100),
    email_contato VARCHAR(100),
    mensagem_contato VARCHAR(500)
""")


    conn.commit()
    cursor.close()
    conn.close()


############################################################

# Inserindo dados
def add_usuario(nome, email, senha, data_nascimento):

    conn = get_db_connection()
    cursor = conn.cursor()


    #verificar se o email ja existe

    cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
    usuario_existente = cursor.fetchall()

    if usuario_existente:
        cursor.close()
        conn.close()
        return False

    cursor.execute("""
    INSERT INTO usuario (nome, email ,senha, data_nascimento) 
    VALUES (%s, %s, %s, %s)
    """, (nome, email, senha, data_nascimento))

    conn.commit()
    cursor.close()
    conn.close()
    return True


#######################################################

#colocar o contato no banco de dado 



def add_contato(name_contato, email_contato, mensagem_contato):

    conn = get_db_connection()
    cursor = conn.cursor()

    #verifiar se o email de contato ja existe no banco de dados

    cursor.execute("SELECT * FROM contato WHERE email_contato = %s", (email_contato,))
    email_contato_existente = cursor.fetchall()


    if email_contato_existente:
        cursor.close()
        conn.close()
        return False



    cursor.execute("""
    INSERT INTO contato (name_contato, email_contato, mensagem_contato)
    VALUES (%s, %s, %s)
""", (name_contato, email_contato, mensagem_contato))
    
    conn.commit()
    cursor.close()
    conn.close()
    return True


#########################################################

def get_usuario():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()
    return usuarios



#######################################################

def add_evento(titulo, descricao_evento, data_evento, id_usuario):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO evento (titulo, descricao_evento, data_evento, id_usuario) 
    VALUES (%s, %s, %s, %s)
    """, (titulo, descricao_evento, data_evento, id_usuario))

    conn.commit()
    cursor.close()
    conn.close()


#########################################################

def get_evento():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM evento")
    eventos = cursor.fetchall()

    cursor.close()
    conn.close()
    return eventos

##########################################################

def verificar_login(email, senha):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute('SELECT id, email, senha FROM usuario WHERE email = %s AND senha = %s', (email, senha))
    user = cursor.fetchall()
    cursor.close()
    conn.close()

    return user

###########################################
def validar_email(email):
    if '@' not in email or '.' not in email:
        return False
    return True

##############################################

def validar_senha(senha):
    if len(senha) < 6:
        return False
    return True

############################################

def validar_nome(nome):

    if len(nome) < 4 or len(nome) > 70:
        return False
    
    if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', nome):
        return False
    
    return True

############################################

def validar_nome_contato(name_contato):

    if len(name_contato) < 4 or len(name_contato) > 70:
        return False
    if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', name_contato):
        return False
    return True

################################################

def validar_email_contato(email_contato):
        if '@' not in email_contato or '.' not in email_contato:
            return False
        return True

###################################################


def validar_mensagem_contato(mensagem_contato):
    if len(mensagem_contato) < 3 or len(mensagem_contato) > 500:
        return False
    return True