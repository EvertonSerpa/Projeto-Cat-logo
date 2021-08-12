from flask import Flask, render_template, request, redirect, url_for, session
from cryptography.fernet import Fernet
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, logout_user, login_user

app = Flask(__name__)

# Configuração do envio de email.
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'blueedtechgrupo3@gmail.com',
    "MAIL_PASSWORD": 'Group3blue'
}

logado = False

app.config.update(mail_settings) #atualizar as configurações do app com o dicionário mail_settings
mail = Mail(app) # atribuir a class Mail o app atual.

## Configuração do app passando os parametros de conexão com o banco de dados sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogo.sqlite'

# #Linha abaixo caso seja necessário utilizar banco de dados postgresql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qlkehnnv:jpzYaAeJILifKKQkh_GQDAi-I2t9YPuu@kesavan.db.elephantsql.com/qlkehnnv'

## Linha remove um warning que fica aparecendo durante a execução do app com sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

## Criação de uma nova instância do SQLAlchemy passando como parametro o app
db = SQLAlchemy(app)
login = LoginManager(app)

##################################################################################
## Definição da classe Horta que herda os comportamentos de db.Model. Dessa forma
## a classe começa a se comportar como um Model que vai fazer o mapeamento com o
## banco de dados. Sintaxe compativel com outros bancos, então se haver uma mudança
## nesse requisito é so alterar o config acima e passar a configuração do banco
## desejado.
##
## Na classe estou definindo que o banco vai ter um id do tipo inteiro que será
## autoincrementado e é uma chave primária. Seguido de um nome tipo String de tamanho
## 25 e não pode ser nulo. Após isso temos a coluna quantidade e valor, definidos
## respectivamente como inteiro e valor em ponto flutuante (número real). e Por fim
## uma coluna img que vai gravar a localização da imagem.
##
## Mais abaixo o método contrutor da classe que recebe nome, quantidade, valor e img
## como parametros e os atribui aos valores do ao seu devido campo no banco de dados
class Horta(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(25), nullable=False)
    tipo = db.Column(db.String(25), nullable=True)
    quantidade = db.Column(db.Integer, nullable=True)
    valor = db.Column(db.Float, nullable=True)
    imagem = db.Column(db.String, nullable=True)

    def __init__(self, nome, tipo, quantidade, valor, img) -> None:
        super().__init__()
        self.nome = nome
        self.tipo = tipo
        self.quantidade = quantidade
        self.valor = valor
        self.imagem = img
##################################################################################


#######Classe#########
class Contato():
    def __init__ (self, nome, email, mensagem):
      self.nome = nome
      self.email = email
      self.mensagem = mensagem


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    key = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, fname, lname, email, password) -> None:
        super().__init__()
        self.firstname = fname
        self.lastname= lname
        self.email = email
        self.password = password
        self.key = Fernet.generate_key()

    def encrypt_pwd(self) -> None:
        f = Fernet(self.key)
        self.password = f.encrypt(self.password.encode(encoding="UTF-8", errors="strict"))

    def decrypt_pwd(self) -> bytes:
        f = Fernet(self.key)
        return f.decrypt(self.password)

    def check_password(self, pwd) -> bool:
        return pwd == self.decrypt_pwd().decode()



######### Rotas #########

# Rota de envio de email.

## Index 
@app.route('/')
def index():
    return render_template('index.html')

### Time ####

@app.route('/time')
def time():
    return render_template('time.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
   if request.method == 'POST':
      # Capiturando as informações do formulário com o request do Flask e criando o objeto formContato
      formContato = Contato(
         request.form['nome'],
         request.form['email'],
         request.form['mensagem']
      )

      # Criando o objeto msg, que é uma instancia da Class Message do Flask_Mail
      msg = Message(
         subject= 'Contate o nosso time ', #Assunto do email
         sender=app.config.get("MAIL_USERNAME"), # Quem vai enviar o email, pega o email configurado no app (mail_settings)
         recipients=[app.config.get("MAIL_USERNAME")], # Quem vai receber o email, mando pra mim mesmo, posso mandar pra mais de um email.
         # Corpo do email.
         body=f'''O {formContato.nome} com o email {formContato.email}, te mandou a seguinte mensagem: 
         
               {formContato.mensagem}''' 
        )
      mail.send(msg) #envio efetivo do objeto msg através do método send() que vem do Flask_Mail
   return render_template('send.html', formContato=formContato) # Renderiza a página de confirmação de envio.

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user = User(
            request.form['firstname'],
            request.form['lastname'],
            request.form['email'],
            request.form['password']
        )

        user.encrypt_pwd()
        db.session.add(user)
        db.session.commit()
        return redirect('/')

    return render_template('cadastro.html')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            login_user(user, remember=True)
            db.session.commit()
            logado = True
        return redirect(url_for('catalogo'))

## Rota catalogo onde é exibido os items cadastrado no catalogo | Read do CRUD
@app.route('/catalogo')
def catalogo():
    # Atribuo a variavel horta que vai armazenar uma lista com a consulta ao banco e joga
    # as informações para a página catalogo onde tudo será renderizado
    horta = Horta.query.all()
    return render_template('catalogo.html', infos=horta, logado=logado)

## Routa de adicionar novo item ao catalogo | Create do CRUD
@app.route('/catalogo/adicionar', methods=['GET', 'POST'])
def adicionar():
    # Se for POST pega o que tiver vindo dos campos e adiciona ao objeto prod
    if request.method == 'POST':
        prod = Horta(
            request.form['nome'],
            request.form['tipo'],
            request.form['quantidade'],
            request.form['valor'],
            request.form['imagem']
        )

        # Similar ao git githug, faz um add passando o objeto criado (prod) e em seguida da um commit
        # em seguida redireciona para a rota do catalogo
        db.session.add(prod)
        db.session.commit()
        return redirect('/catalogo')

@app.route('/catalogo/<id>')
def modalInfo(id):
    prod = Horta.query.get(id)
    return render_template('catalogo.html', info=prod)

## Rota de alterar algum item do catálogo passando como parametro o id do item | Update do CRUD
@app.route('/catalogo/edit/<id>', methods=['GET', 'POST'])
def alterar(id):
    # atribuição da consulta ao banco à variavel prod
    prod = Horta.query.get(id)

    # Se for POST é feita a suas devidas alterações e dado um novo commit. Em seguida redireciona
    # para a rota catalogo
    if request.method == 'POST':
        prod.nome = request.form['nome']
        prod.tipo = request.form['tipo']
        prod.quantidade = request.form['quantidade']
        prod.valor = request.form['valor']
        prod.imgaem = request.form['imagem']
        db.session.commit()
        return redirect(url_for('catalogo'))

    return render_template('editar.html', info=prod)

## Rota que remove um item do catálogo passando o id do item como parametro | Delete do CRUD
@app.route('/catalogo/delete/<id>')
def deletar(id):
    # Como nos casos anteriores, é feito uma consulta no banco passando o id do item como
    # paramentro e o resultado é armazenado na variável prod. Então é feito um delete no prod
    # e dado um novo commit. Por fim, redireciona à rota catalogo
    prod = Horta.query.get(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect('/catalogo')


# Rota para páginas não encontradas
@app.route('/<slug>')
@app.route('/catalogo/<slug>')
def not_found(slug):
    return render_template('notFound.html', slug=slug)

if __name__ == '__main__':
    # comando para criar o banco de dados
    # db.drop_all()
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=3000)