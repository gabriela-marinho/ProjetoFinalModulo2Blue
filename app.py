from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

# Modelar a Classe Filmes -> tabela filmes
class racas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    imagem = db.Column(db.String(255), nullable=False)

    def __init__(self, nome, imageml):
        self.nome = nome
        self.imagem_url = imagem
    
    @staticmethod
    def read_all():
        # SELECT * FROM filmes ORDER BY id ASC
        return racas.query.order_by(racas.id.asc()).all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/read")
def read_all():
    registros = racas.read_all()
    # Chamada do método read_all da classe Filmes, que representa a tabela filmes do banco de dados.
    registros = racas.read_all()
    return render_template("read_all.html", registros=registros)


@app.route("/read/<id_registro>")
def read_id(id_registro):
    return "Em construção - Visualizar registro de ID "+id_registro


@app.route("/create")
def create():
    return "Em construção - Ainda será feito o CREATE!"


if (__name__ == "__main__"):
    app.run(debug=True)