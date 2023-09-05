# coding: utf-8

# todos os imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuração
DATABASE = 'tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

# criar nossa pequena aplicação :)
app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('CONFIG_FLASKR', silent=True)

def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

def criar_bd():
    with closing(conectar_bd()) as bd:
        with app.open_resource('esquema.sql') as sql:
            script = sql.read().decode('utf-8')
            bd.cursor().executescript(script)
        bd.commit()

@app.before_request
def pre_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def encerrar_requisicao(exception):
    g.bd.close()

@app.route('/')
def exibir_entradas():
    sql = '''select titulo, texto from entradas order by id desc'''
    cur = g.bd.execute(sql)
    entradas = [dict(titulo=titulo, texto=texto)
                for titulo, texto in cur.fetchall()]
    return render_template('exibir_entradas.html', entradas=entradas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Usuário inválido'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Senha inválida'
        else:
            session['logado'] = True
            flash('Login OK')
            return redirect(url_for('exibir_entradas'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logado', None)
    flash('Logout OK')
    return redirect(url_for('exibir_entradas'))

@app.route('/inserir_entrada', methods=['POST'])
def inserir_entrada():
    if not session.get('logado'):
        abort(401)

    titulo = request.form['titulo']
    texto = request.form['texto']
    
    # Lógica para inserir uma nova entrada no banco de dados
    # Certifique-se de adaptar esta lógica à sua estrutura de banco de dados
    with conectar_bd() as bd:
        bd.execute('INSERT INTO entradas (titulo, texto) VALUES (?, ?)', (titulo, texto))
        bd.commit()

    flash('Entrada inserida com sucesso!')
    return redirect(url_for('exibir_entradas'))

if __name__ == '__main__':
    app.run()
