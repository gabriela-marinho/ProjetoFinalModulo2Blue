from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import RequestCacheControl

app = Flask(__name__)

# Configurações de acesso ao banco de dados
user = 'uutnfujn'
password = 'TJ-budc9lkNSwDgt29vxcSjalpXx2bj7'
host = 'tuffi.db.elephantsql.com'
database = 'uutnfujn'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "chave escondidamente"

# Instanciando objeto da classe SQLAlchemy
db = SQLAlchemy(app)

# Modelar a Classe Filmes -> tabela racas
class racas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    imagem = db.Column(db.String(255), nullable=False)
    curiosidade = db.Column(db.String(10000),nullable=False)

    def __init__(self, nome, imagem, curiosidade):
        self.nome = nome
        self.imagem = imagem
        self.curiosidade = curiosidade
    # o static usa ,geralmente em uma manipulaçao que vai trazer algum registro do banco
    @staticmethod
    def read_all():
        # SELECT * FROM filmes ORDER BY id ASC
        return racas.query.order_by(racas.id.asc()).all()
    db = SQLAlchemy(app)

    @staticmethod
    def read_single(id_registro):
        # SELECT * FROM filmes ORDER BY id ASC
        return racas.query.get(id_registro)
    db = SQLAlchemy(app)    
    

    def save(self): #função para salvar os dados inserido via input no bd, 
    #não é staticmethod pq nao precisa de uma qyuery para ser chamado e adicionado
        db.session.add(self)
        db.session.commit()

    def update(self,novo_nome,novo_imagem,novo_curiosidade):
        self.nome = novo_nome
        self.imagem = novo_imagem
        self.curiosidade = novo_curiosidade
        self.save()
        
    def delete(self):   # funcao que vai apagar o registro recebido pelo usuario na pagina pelo botão excluir 
        db.session.delete(self)
        db.session.commit()       

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/read")
def read_all():
    registros = racas.read_all()
    # Chamada do método read_all da classe racas, que representa a tabela racas do banco de dados.
    registros = racas.read_all()
    return render_template("read_all.html", registros=registros)


@app.route("/read/<id_registro>")
def read_id(id_registro):
    registro= racas.read_single(id_registro)
    return render_template("read_single.html", registro=registro)


@app.route("/create", methods=('GET', 'POST'))
def create():
    id_registro_novo = None # cria uma variável nula para o novo ID atribuído

    if request.method == 'POST': # verifica se está recebendo alguma coisa por POST
        form = request.form # armazena o formulário recebido por POST

        registro = racas(form['nome'], form['imagem'],form['curiosidade']) # cria um novo registro (objeto) com nome e imagem_url recebidos
        registro.save() # chama a função save da classe (adiciona e commita)

        id_registro_novo = registro.id # atribui a novo_id o ID do novo registro criado

    return render_template("create.html",id_registro_novo = id_registro_novo) # carrega o create.html passando o valor de novo_id (None ou novo ID atribuído)

@app.route("/update/<id_registro>", methods=('GET', 'POST'))
def update(id_registro):
    sucesso = False # se foi alterado com sucesso ou nao
    registro= racas.read_single(id_registro)

    if request.method == 'POST':
        form = request.form
        registro.update(form['nome'], form['imagem'],form['curiosidade'])
        # # novo_registro = racas(form['nome'], form['imagem'],form['curiosidade'])
        # registro.update(novo_registro)
        sucesso = True
    return render_template('update.html',registro=registro,sucesso=sucesso) 

@app.route('/delete/<id_registro>')
def delete(id_registro):
    registro= racas.read_single(id_registro)
    return render_template('delete.html', registro=registro)

@app.route('/delete/<id_registro>/confirmed')
def delete_confirmed(id_registro):
    confirmar = False

    registro= racas.read_single(id_registro)

    if registro:
        registro.delete()
        confirmar=True

    return render_template('delete.html',registro=registro,confirmar=confirmar)  



if (__name__ == "__main__"):
    app.run(debug=True)
