from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Configuração do envio de email.
mail_settings = {
    "MAIL_SERVER": 'smtp.mailtrap.io',
    "MAIL_PORT": 2525,
    "MAIL_USERNAME": '5622d2e98706a9',
    "MAIL_PASSWORD": 'f296da83b42768',
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
   #  "MAIL_USERNAME": email,
   #  "MAIL_PASSWORD": mail_senha
}

app.config.update(mail_settings) #atualizar as configurações do app com o dicionário mail_settings
mail = Mail(app) # atribuir a class Mail o app atual.

## Configuração do app passando os parametros de conexão com o banco de dados sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qlkehnnv:jpzYaAeJILifKKQkh_GQDAi-I2t9YPuu@kesavan.db.elephantsql.com/qlkehnnv'

# #Linha abaixo caso seja necessário utilizar banco de dados postgresql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postegresql://username:password@hostname-or-url/db-name'

## Linha remove um warning que fica aparecendo durante a execução do app com sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

## Criação de uma nova instância do SQLAlchemy passando como parametro o app
db = SQLAlchemy(app)

#Teste

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
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.Float)
    img = db.Column(db.Text)

    def __init__(self, tipo, nome, quantidade, valor, img) -> None:
        super().__init__()
        self.tipo = tipo
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        self.img = img
##################################################################################


#######Classe#########
class Contato:
   def __init__ (self, nome, email, mensagem):
      self.nome = nome
      self.email = email
      self.mensagem = mensagem
#########Rota#########

# Rota de envio de email.
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
         subject= 'Contato do seu Portfólio', #Assunto do email
         sender=app.config.get("MAIL_USERNAME"), # Quem vai enviar o email, pega o email configurado no app (mail_settings)
         recipients=[app.config.get("MAIL_USERNAME"),'renan_jc9@yahoo.com.br','josep.macedo@outlook.com'], # Quem vai receber o email, mando pra mim mesmo, posso mandar pra mais de um email.
         # Corpo do email.
         body=f'''O {formContato.nome} com o email {formContato.email}, te mandou a seguinte mensagem: 
         
               {formContato.mensagem}''' 
         )
      mail.send(msg) #envio efetivo do objeto msg através do método send() que vem do Flask_Mail
   return render_template('send.html', formContato=formContato) # Renderiza a página de confirmação de envio.

## Index
@app.route('/')
def index():
    return render_template('index.html')

## Rota catalogo onde é exibido os items cadastrado no catalogo | Read do CRUD
@app.route('/catalogo')
def catalogo():
    # Atribuo a variavel horta que vai armazenar uma lista com a consulta ao banco e joga
    # as informações para a página catalogo onde tudo será renderizado
    horta = Horta.query.all()
    return render_template('catalogo.html', infos=horta)

## Routa de adicionar novo item ao catalogo | Create do CRUD
@app.route('/catalogo/adicionar', methods=['GET', 'POST'])
def adicionar():

    # verifica o tempo de requisição, se for GET renderiza a tela de adicionar produto
    if request.method == 'GET':
        return render_template('adicionar.html')
    
    # Se for POST pega o que tiver vindo dos campos e adiciona ao objeto prod
    elif request.method == 'POST':
        prod = Horta(
            request.form['tipo'],
            request.form['name'],
            request.form['quantidade'],
            request.form['valor'],
            request.form['image']
        )

        # Similar ao git githug, faz um add passando o objeto criado (prod) e em seguida da um commit
        # em seguida redireciona para a rota do catalogo
        db.session.add(prod)
        db.session.commit()
        return redirect('/catalogo')

    # Else apenas para saciar o toc, nunca vai cair aqui
    else:
        pass

## Rota de alterar algum item do catálogo passando como parametro o id do item | Update do CRUD
@app.route('/catalogo/alterar/<id>', methods=['GET', 'POST'])
def alterar(id):
    # atribuição da consulta ao banco à variavel prod
    prod = Horta.query.get(id)

    # Assim como na rota adicionar, vericica se a requisição é 'GET' ou 'POST. Se for
    # GET, renderiza a tela de alteração do item junto com as informações do consulta
    # armazenado em prod
    if request.method == 'GET':
        return render_template('alterar.html', info=prod)
    
    # Se for POST é feita a suas devidas alterações e dado um novo commit. Em seguida redireciona
    # para a rota catalogo
    elif request.method == 'POST':
        prod.tipo = request.form['tipo']
        prod.nome = request.form['name']
        prod.quantidade = request.form['quantidade']
        prod.valor = request.form['valor']
        prod.img = request.form['image']
        db.session.commit()
        return redirect('/catalogo')

    # TOC
    else:
        pass

## Rota que remove um item do catálogo passando o id do item como parametro | Delete do CRUD
@app.route('/catalogo/deletar/<id>')
def deletar(id):
    # Como nos casos anteriores, é feito uma consulta no banco passando o id do item como
    # paramentro e o resultado é armazenado na variável prod. Então é feito um delete no prod
    # e dado um novo commit. Por fim, redireciona à rota catalogo
    prod = Horta.query.get(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect('/catalogo')

## Rota que leva a página Sobre com as informações dos desenvolvedores
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


if __name__ == '__main__':
    # comando para criar o banco de dados
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=3000)