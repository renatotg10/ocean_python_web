from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro1')
def cadastro1():
    return render_template('cadastro1.html')

@app.route('/cadastro2')
def cadastro2():
    return render_template('cadastro2.html')

if __name__ == '__main__':
    app.run(debug=True)
