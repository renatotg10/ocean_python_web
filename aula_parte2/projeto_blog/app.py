from flask import Flask, render_template

app = Flask(__name__)

# Dicionário de postagens do blog (substitua com suas próprias postagens)
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

@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run(debug=True)
