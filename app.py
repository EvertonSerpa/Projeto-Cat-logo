from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Horta(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(25), nullable=False)
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.Float)
    img = db.Column(db.Text)

    def __init__(self, nome, quantidade, valor, img) -> None:
        super().__init__()
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        self.img = img

def create_database():
    db.create_all()

def drop_database():
    db.drop_all()

# create_database()
# drop_database()

@app.route('/')
def index():
    horta = Horta.query.all()
    return render_template('index.html', infos=horta)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'GET':
        return render_template('adicionar.html')
    elif request.method == 'POST':
        prod = Horta(
            request.form['name'],
            request.form['quantidade'],
            request.form['valor'],
            request.form['image']
        )
        db.session.add(prod)
        db.session.commit()
        return redirect('/')

@app.route('/alterar/<id>', methods=['GET', 'POST'])
def alterar(id):
    prod = Horta.query.get(id)
    if request.method == 'GET':
        return render_template('alterar.html', info=prod)
    
    elif request.method == 'POST':
        prod.nome = request.form['name']
        prod.quantidade = request.form['quantidade']
        prod.valor = request.form['valor']
        prod.img = request.form['image']
        db.session.commit()
        return redirect('/')

    else:
        pass

@app.route('/deletar/<id>')
def deletar(id):
    prod = Horta.query.get(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)