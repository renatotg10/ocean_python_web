# Blog em Flask

Este é um exemplo simples de um aplicativo web usando o framework Flask em Python. O aplicativo cria um blog básico com três postagens de blog de exemplo e três páginas: Página Inicial, Sobre e Contato.

## Configuração do Projeto

Antes de começar, certifique-se de que você tenha Flask instalado em seu ambiente de desenvolvimento. Se ainda não tiver, você pode instalá-lo com o comando:

```bash
pip install Flask
pip install python-dotenv
```

## Entendendo o Código

Aqui está uma explicação detalhada do código em `app.py`:

1. **Importações**:

   ```python
   from flask import Flask, render_template
   ```

   - Importamos a classe `Flask` do framework Flask, que nos permite criar um aplicativo web.
   - Importamos `render_template`, que nos permite renderizar páginas HTML usando templates.

2. **Criação de uma instância Flask**:

   ```python
   app = Flask(__name__)
   ```

   - Criamos uma instância Flask chamada `app`.

3. **Dicionário de Postagens do Blog**:

   ```python
   blog_posts = [
       {
           'titulo': 'Postagem 1',
           'texto': 'Este é o conteúdo da postagem 1.'
       },
       {
           'titulo': 'Postagem 2',
           'texto': 'Este é o conteúdo da postagem 2.'
       },
       {
           'titulo': 'Postagem 3',
           'texto': 'Este é o conteúdo da postagem 3.'
       }
   ]
   ```

   - Criamos um dicionário que contém três postagens de blog de exemplo. Você pode substituir essas postagens por suas próprias postagens.

4. **Rotas e Funções**:

   - Definimos três rotas no aplicativo Flask:

     - A rota `'/'` renderiza a página inicial (`index.html`) e passa as postagens do blog para a página.
     - A rota `'/sobre'` renderiza a página "Sobre".
     - A rota `'/contato'` renderiza a página "Contato".

5. **Execução do Aplicativo**:

   ```python
   if __name__ == '__main__':
       app.run(debug=True)
   ```

   - Inicializamos o aplicativo somente se o script estiver sendo executado diretamente (não se for importado como um módulo). A configuração `debug=True` permite que o aplicativo seja executado em modo de depuração.

## Templates HTML

Aqui estão os códigos dos templates HTML que são usados no aplicativo:

### `layout.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Meu Site{% endblock %}</title>
    <!-- Inclua o link para o Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
</head>
<body>
    <header>
        <!-- Bootstrap Navbar -->
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container">
                <a class="navbar-brand" href="/">Meu Site</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Página Inicial</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/sobre">Sobre</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/contato">Contato</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <main>
        {% block content %}
        <!-- Conteúdo da página vai aqui -->
        {% endblock %}
    </main>

    <footer class="text-center bg-dark text-white p-3 fixed-bottom">
        <p class="m-0">&copy; 2023 Meu Blog</p>
    </footer>    

    <!-- Inclua os scripts JavaScript do Bootstrap 5 -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
</body>
</html>
```

### `index.html`

```html
{% extends 'layout.html' %}

{% block content %}
<div class="container mt-5">
    <h2 class="display-4">Bem-vindo ao Meu Blog</h2>
    <div class="row">
        {% for post in posts %}
        <div class="col-md-4 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{ post['titulo'] }}</h5>
                    <p class="card-text">{{ post['texto'] }}</p>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### `sobre.html`

```html
{% extends 'layout.html' %}

{% block content %}
<div class="container mt-5">
    <h1>Sobre Nós</h1>

    <h2>Bem-vindo ao nosso blog!</h2>
    <p>Somos um grupo apaixonado por compartilhar conhecimento e experiências com você. Nossa missão é fornecer conteúdo relevante, informativo e interessante para ajudar você a aprender e crescer.</p>

    <h3>O Que Você Pode Esperar</h3>
    <p>No nosso blog, você encontrará uma variedade de tópicos abrangentes. Desde dicas úteis para o dia a dia até discussões aprofundadas sobre temas específicos, estamos aqui para proporcionar uma experiência enriquecedora de leitura.</p>

    <h3>Nossos Autores</h3>
    <p>Nossa equipe é composta por indivíduos dedicados e especializados em diversas áreas. Cada autor traz seu conhecimento e paixão para criar conteúdo que seja informativo e envolvente.</p>

    <h3>Interaja Conosco</h3>
    <p>Adoramos ouvir o que você tem a dizer! Sinta-se à vontade para comentar em nossas postagens, compartilhar suas opiniões e fazer perguntas. Acreditamos que a interação com nossa comunidade enriquece a experiência de todos.</p>

    <h3>Obrigado Por Nos Escolher</h3>
    <p>Agradecemos por escolher nosso blog como sua fonte de informação e entretenimento. Esperamos que você aproveite a jornada conosco e que nossas postagens sejam úteis e inspiradoras.</p>
</div>
{% endblock %}
```

### `contato.html`

```html
{% extends 'layout.html' %}

{% block content %}
<div class="container mt-5">
    <h2 class="display-4">Entre em Contato</h2>
    <p>
        Você pode entrar em contato conosco de várias maneiras. Estamos sempre felizes em ouvir de você!
    </p>
    <ul>
        <li><strong>Email:</strong> exemplo@email.com</li>
        <li><strong>Telefone:</strong> (XX) XXXX-XXXX</li>
    </ul>
    <p>
        Ou, se preferir, você pode preencher o formulário abaixo e responderemos o mais rápido possível:
    </p>
    <!-- Adicione aqui o seu formulário de contato, se tiver um -->
</div>
{% endblock %}
```

## Executando o Aplicativo

Para iniciar o aplicativo, execute o arquivo `app.py`. O servidor Flask começará a ser executado localmente em `http://localhost:5000/`. Você pode acessar as seguintes páginas:

- Página Inicial: `http://localhost:5000/`
- Página Sobre: `http://localhost:5000/sobre`
- Página Contato: `http://localhost:5000/contato`

```

Esta é uma explicação detalhada do código do seu aplicativo Flask, incluindo os templates HTML. Certifique-se de substituir as postagens de exemplo pelo seu próprio conteúdo e personalizar o aplicativo de acordo com suas necessidades.