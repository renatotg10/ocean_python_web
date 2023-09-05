# Aplicação Flaskr - Blog Simples
04/09/2023 - Renato Teixeira Gomes - renatotg10@gmail.com
Documento elaborado com auxílio do ChatGPT (https://chat.openai.com/)

### Documentação original do projeto da aplicação Flaskr
http://turing.com.br/material/flask/tutorial/introduction.html

## Visão Geral

Este é um tutorial detalhado sobre como criar uma aplicação web simples chamada Flaskr, que funciona como um blog. A aplicação permite que os usuários visualizem postagens, façam login, publiquem novas entradas e façam logout. Vamos explorar cada parte do código e as etapas para executar a aplicação.

## Estrutura do Projeto

A estrutura do projeto inclui os seguintes arquivos e pastas:

- **flaskr.py**: O arquivo principal que contém o código da aplicação Flask.
- **esquema.sql**: Um arquivo SQL que define a estrutura da tabela de postagens do blog.
- **.flaskenv**: Um arquivo que configura o ambiente Flask, especificando o arquivo principal e habilitando o modo de depuração.
- **templates**: Uma pasta que contém os templates HTML usados na aplicação.
- **static/estilo.css**: Um arquivo CSS para estilizar as páginas HTML.
- **tmp/flaskr.db**: Um banco de dados SQLite onde as postagens do blog são armazenadas.

## Configuração do Projeto

Antes de começar, certifique-se de que você tenha Flask instalado em seu ambiente de desenvolvimento. Se ainda não tiver, você pode instalá-lo com o comando:

```bash
pip install Flask
pip install python-dotenv
```

### Configurando o ambiente de desenvolvimento do Flask

Na pasta raiz do projeto, crie um arquivo com nome `.flaskenv` e adicione o conteúdo abaixo nele:

```
FLASK_APP=flaskr.py
FLASK_DEBUG=1
```

O arquivo `.flaskenv` é usado para configurar o ambiente de desenvolvimento do Flask. Nele, você pode definir variáveis de ambiente específicas para o Flask, que serão carregadas automaticamente quando você executar a aplicação Flask usando o comando `flask run`.

Neste caso, as duas variáveis de ambiente definidas no `.flaskenv` são:

1. `FLASK_APP=flaskr.py`: Essa variável especifica o arquivo principal da sua aplicação Flask. O Flask utiliza essa informação para identificar qual arquivo deve ser considerado o ponto de entrada da aplicação. No seu caso, `flaskr.py` é o arquivo principal que contém a aplicação Flask.

2. `FLASK_DEBUG=1`: Essa variável habilita o modo de depuração do Flask. Quando o modo de depuração está ativado (com o valor `1`), a aplicação Flask reinicia automaticamente sempre que você faz uma alteração no código, facilitando o desenvolvimento e a depuração. Além disso, ele fornece mensagens detalhadas de erro no navegador em caso de exceções.

Em resumo, o `.flaskenv` é usado para configurar as variáveis de ambiente específicas do Flask, tornando o processo de desenvolvimento mais conveniente e eficiente. Certifique-se de que o Flask seja compatível com o uso do arquivo `.flaskenv` para carregar essas configurações automaticamente, pois essa funcionalidade pode variar dependendo da versão do Flask ou das configurações do seu ambiente de desenvolvimento.


### Script SQL para criação da tabela `entradas`

Na pasta raiz do projeto, crie um arquivo com nome `esquema.sql` e adicione o conteúdo abaixo nele:

```sql
drop table if exists entradas;
create table entradas (
  id integer primary key autoincrement,
  titulo string not null,
  texto string not null
);
```

### `flaskr.py`:

```python
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

# Funções para conectar e criar o banco de dados
def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

def criar_bd():
    with closing(conectar_bd()) as bd:
        with app.open_resource('esquema.sql') as sql:
            script = sql.read().decode('utf-8')
            bd.cursor().executescript(script)
        bd.commit()

# Antes de cada requisição
@app.before_request
def pre_requisicao():
    g.bd = conectar_bd()

# Após cada requisição
@app.teardown_request
def encerrar_requisicao(exception):
    g.bd.close()

# Rota para exibir as entradas
@app.route('/')
def exibir_entradas():
    sql = '''select titulo, texto from entradas order by id desc'''
    cur = g.bd.execute(sql)
    entradas = [dict(titulo=titulo, texto=texto)
                for titulo, texto in cur.fetchall()]
    return render_template('exibir_entradas.html', entradas=entradas)

# Rota para fazer login
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

# Rota para fazer logout
@app.route('/logout')
def logout():
    session.pop('logado', None)
    flash('Logout OK')
    return redirect(url_for('exibir_entradas'))

# Rota para inserir entrada (requer login)
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

# Executa a aplicação se o script for executado diretamente
if __name__ == '__main__':
    app.run()
```

### Explicando cada parte do código em detalhes:

1. **Imports e Configurações Iniciais**:

   ```python
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
   ```

   - O código começa com uma série de imports necessários. Flask é o principal framework usado para criar a aplicação web.
   - As configurações iniciais são definidas, incluindo o local do banco de dados, configurações de depuração e informações de autenticação (usuário e senha para login).

2. **Criação da Aplicação Flask**:

   ```python
   # criar nossa pequena aplicação :)
   app = Flask(__name__)
   app.config.from_object(__name__)
   # app.config.from_envvar('CONFIG_FLASKR', silent=True)
   ```

   - Uma instância do Flask é criada com o nome da aplicação. Esta instância será usada para configurar e executar a aplicação.

3. **Funções de Banco de Dados**:

   ```python
   # Funções para conectar e criar o banco de dados
   def conectar_bd():
       return sqlite3.connect(app.config['DATABASE'])

   def criar_bd():
       with closing(conectar_bd()) as bd:
           with app.open_resource('esquema.sql') as sql:
               script = sql.read().decode('utf-8')
               bd.cursor().executescript(script)
           bd.commit()
   ```

   - `conectar_bd()`: Esta função cria e retorna uma conexão com o banco de dados SQLite definido na configuração.
   - `criar_bd()`: Esta função é usada para criar a estrutura do banco de dados, lendo um arquivo SQL chamado `esquema.sql` e executando as instruções contidas nele.

4. **Callbacks do Flask**:

   ```python
   # Antes de cada requisição
   @app.before_request
   def pre_requisicao():
       g.bd = conectar_bd()

   # Após cada requisição
   @app.teardown_request
   def encerrar_requisicao(exception):
       g.bd.close()
   ```

   - `@app.before_request`: Este decorator define uma função que será executada antes de cada requisição à aplicação. Neste caso, ele cria uma conexão com o banco de dados antes de cada requisição e a armazena em `g.bd`.
   - `@app.teardown_request`: Este decorator define uma função que será executada após cada requisição. Neste caso, ele fecha a conexão com o banco de dados após a requisição.

5. **Rotas e Funções**:

   - A aplicação Flask define várias rotas e funções para lidar com diferentes partes da aplicação, como login, logout, exibição de postagens e inserção de novas postagens. Vou explicar algumas das principais rotas:

     - `/`: A rota raiz da aplicação, que exibe as postagens do blog.
     - `/login`: A rota para fazer login na aplicação.
     - `/logout`: A rota para fazer logout.
     - `/inserir_entrada`: A rota para inserir uma nova entrada no blog.

6. **Execução da Aplicação**:

   ```python
   # Executa a aplicação se o script for executado diretamente
   if __name__ == '__main__':
       app.run()
   ```

   - Esta parte do código verifica se o script está sendo executado diretamente (não importado como um módulo) e, se for o caso, inicia a aplicação Flask.

## Funcionalidades Principais

Aqui estão as principais funcionalidades implementadas na aplicação Flaskr:

### Página Inicial

- A página inicial exibe todas as postagens do blog em ordem decrescente de data.
- Os usuários podem visualizar as postagens mesmo sem fazer login.

### Login e Logout

- A página de login permite que os usuários façam login com um nome de usuário e senha.
- Se o login for bem-sucedido, os usuários serão redirecionados para a página inicial e receberão uma mensagem de sucesso.
- Os usuários podem fazer logout a qualquer momento, o que os desconectará da sessão.

### Inserir Entrada

- Os usuários autenticados podem inserir novas entradas no blog.
- Eles podem fornecer um título e um texto para a nova entrada.
- As novas entradas são inseridas no banco de dados e são exibidas na página inicial após a inserção bem-sucedida.

## Templates HTML

A aplicação usa templates HTML para renderizar páginas. Aqui estão os principais templates:

### `layout.html`

```html
<!doctype html>
<title>Flaskr</title>
<link rel="stylesheet" type="text/css"
      href="{{ url_for('static', filename='estilo.css') }}">
<div class="pagina">
  <h1>Flaskr</h1>
  <div class="metanav">
  {% if not session.logado %}
    <a href="{{ url_for('login') }}">login</a>
  {% else %}
    <a href="{{ url_for('logout') }}">logout</a>
  {% endif %}
  </div>
  {% for mensagem in get_flashed_messages() %}
    <div class="flash">{{ mensagem }}</div>
  {% endfor %}
  {% block corpo %}{% endblock %}
</div>
```

### `login.html`

```html
{% extends "layout.html" %}
{% block corpo %}
  <h2>Login</h

2>
  {% if erro %}<p class="erro"><strong>Erro:</strong> {{ erro }}{% endif %}
  <form action="{{ url_for('login') }}" method="post">
    <dl>
      <dt>Username:
      <dd><input type="text" name="username">
      <dt>Password:
      <dd><input type="password" name="password">
      <dd><input type="submit" value="Login">
    </dl>
  </form>
{% endblock %}
```

### `exibir_entradas.html`

```html
{% extends "layout.html" %}
{% block corpo %}
  {% if session.logado %}
    <form action="{{ url_for('inserir_entrada') }}" method="post"
          class="ins-entrada">
      <dl>
        <dt>Título:
        <dd><input type="text" size="30" name="titulo">
        <dt>Texto:
        <dd><textarea rows="5" cols="40" name="texto"></textarea>
        <dd><input type="submit" value="Publicar">
      </dl>
    </form>
  {% endif %}
  <ul class="entradas">
  {% for entrada in entradas %}
    <li><h2>{{ entrada.titulo }}</h2>{{ entrada.texto|safe }}
  {% else %}
    <li><em>Inacreditável. Até agora nenhuma entrada.</em>
  {% endfor %}
  </ul>
{% endblock %}
```

### `estilo.css`

```css
body            { font-family: sans-serif; background: #eee; }
a, h1, h2       { color: #377BA8; }
h1, h2          { font-family: 'Georgia', serif; margin: 0; }
h1              { border-bottom: 2px solid #eee; }
h2              { font-size: 1.2em; }

.pagina         { margin: 2em auto; width: 35em; border: 5px solid #ccc;
                  padding: 0.8em; background: white; }
.entradas       { list-style: none; margin: 0; padding: 0; }
.entradas li    { margin: 0.8em 1.2em; }
.entradas li h2 { margin-left: -1em; }
.ins-entrada    { font-size: 0.9em; border-bottom: 1px solid #ccc; }
.ins-entrada dl { font-weight: bold; }
.metanav        { text-align: right; font-size: 0.8em; padding: 0.3em;
                  margin-bottom: 1em; background: #fafafa; }
.flash          { background: #CEE5F5; padding: 0.5em;
                  border: 1px solid #AACBE2; }
.erro           { background: #F0D6D6; padding: 0.5em; }
```

## Executando a Aplicação

Para executar a aplicação Flaskr, siga estas etapas:

1. Certifique-se de ter o Flask instalado em seu ambiente de desenvolvimento.

   ```bash
   pip install Flask
   ```
2. Crie o arquivo de banco de dados SQLite `flaskr.db`.

  Acesse o console do Python, para isso, no terminal digite o comando `python` e pressione enter. Ao acessar o console do Python, o propmt do terminal irá ficar com o símbolo `>>>`.

  Para criar o arquivo do banco de dados `/tmp/flaskr.db`, você deve chamar explicitamente a função `criar_bd()`. No console do Python execute os seguintes comandos:

  ```python
  from flaskr import criar_bd
  criar_bd()
  ```

  Certifique-se de que o arquivo 'esquema.sql' esteja presente no mesmo diretório em que o arquivo `flaskr.py` está localizado e que não contenha erros de sintaxe SQL. Após a execução desses comandos, o arquivo `/tmp/flaskr.db` deve ser criado com base no conteúdo do arquivo 'esquema.sql'. Certifique-se de verificar se o diretório `/tmp` existe no sistema de arquivos e se você tem permissões de escrita nele.

3. Execute o arquivo `flaskr.py`.

   ```bash
   python flaskr.py
   ```

A aplicação será executada localmente em `http://localhost:5000/`.

## Conclusão

Este tutorial detalhou a criação da aplicação Flaskr, um blog simples, usando o Flask. Você pode explorar e modificar este projeto para criar sua própria aplicação web baseada em Flask. Certifique-se de adaptar a lógica de inserção de entradas ao seu próprio banco de dados, se necessário. Divirta-se criando sua aplicação Flask!