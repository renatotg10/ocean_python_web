from flask import Flask, render_template, request, session, abort, flash, redirect, url_for, g
from posts import posts
import sqlite3
import datetime  # Importe datetime aqui

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pudim'

app.config.from_object(__name__)

DATABASE = "banco.bd"

def conectar():
    return sqlite3.connect(DATABASE)

@app.before_request
def pre_requisicao():
    g.bd = conectar()

@app.teardown_request
def encerrar_requisicao(exception):
    g.bd.close()

@app.route('/')
def exibir_entradas():
    sql = "SELECT id, titulo, texto, data_criacao FROM posts ORDER BY id DESC"
    resultado = g.bd.execute(sql)
    entradas = resultado.fetchall()
    return render_template('exibir_entradas.html', entradas=entradas)


@app.route('/login', methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        if request.form['username'] == "admin" and request.form['password'] == "admin":
            session['logado'] = True
            flash("Login efetuado com sucesso!")
            return redirect(url_for('exibir_entradas'))
        erro = "Usuário ou senha inválidos"        
    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.pop('logado')
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('exibir_entradas'))

@app.route('/inserir', methods=["POST"])
def inserir_entradas():
    if session.get('logado'):
        titulo = request.form['titulo']
        texto = request.form['texto']
        data_criacao = datetime.datetime.now()  # Importe datetime se não o fez

        sql = "INSERT INTO posts (titulo, texto, data_criacao) VALUES (?, ?, ?)"
        g.bd.execute(sql, (titulo, texto, data_criacao))
        g.bd.commit()

        flash("Post criado com sucesso!")
    return redirect(url_for('exibir_entradas'))


@app.route('/posts/<int:id>')
def exibir_entrada(id):
    try:
        entrada = posts[id-1]
        return render_template('exibir_entrada.html', entrada=entrada)
    except Exception:
        return abort(404)

@app.route('/excluir/<int:id>', methods=["POST"])
def excluir_entrada(id):
    if session.get('logado'):
        # Aqui você pode adicionar lógica para verificar se o usuário logado tem permissão para excluir a postagem (por exemplo, verificar se o autor da postagem é o usuário logado).
        
        # Execute a consulta SQL para excluir a postagem pelo ID
        sql = "DELETE FROM posts WHERE id = ?"
        g.bd.execute(sql, (id,))
        g.bd.commit()
        
        flash("Postagem excluída com sucesso!")
    
    return redirect(url_for('exibir_entradas'))
