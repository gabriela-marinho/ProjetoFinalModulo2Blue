from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import RequestCacheControl

app = Flask(__name__)


user = 'uutnfujn'
password = 'TJ-budc9lkNSwDgt29vxcSjalpXx2bj7'
host = 'tuffi.db.elephantsql.com'
database = 'uutnfujn'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "chave escondidamente"


db = SQLAlchemy(app)


class racas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    imagem = db.Column(db.String(255), nullable=False)
    curiosidade = db.Column(db.String(10000),nullable=False)

    def __init__(self, nome, imagem, curiosidade):
        self.nome = nome
        self.imagem = imagem
        self.curiosidade = curiosidade
        
    
    @staticmethod
    def read_all():
        
        result = racas.query.order_by(racas.id.asc()).all()
        db.session.close_all()
        return result
    

    @staticmethod
    def read_single(id_registro):
        
        result = racas.query.get(id_registro)
        db.session.close_all()
        return result

    def save(self): 
        db.session.add(self)
        db.session.commit()

    def update(self,novo_nome,novo_imagem,novo_curiosidade):
        self.nome = novo_nome
        self.imagem = novo_imagem
        self.curiosidade = novo_curiosidade
        self.save()
        
    def delete(self):   
        db.session.delete(self)
        db.session.commit()
        db.session.close_all()       

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/read")
def read_all():
    registros = racas.read_all()
    
    registros = racas.read_all()
    return render_template("read_all.html", registros=registros)


@app.route("/read/<id_registro>")
def read_id(id_registro):
    registro= racas.read_single(id_registro)
    return render_template("read_single.html", registro=registro)


@app.route("/create", methods=('GET', 'POST'))
def create():
    id_registro_novo = None 

    if request.method == 'POST': 
        form = request.form 

        registro = racas(form['nome'], form['imagem'],form['curiosidade']) 
        registro.save() 

        id_registro_novo = registro.id 

    return render_template("create.html",id_registro_novo = id_registro_novo) 

@app.route("/update/<id_registro>", methods=('GET', 'POST'))
def update(id_registro):
    sucesso = False 
    registro= racas.read_single(id_registro)

    if request.method == 'POST':
        form = request.form
        registro.update(form['nome'], form['imagem'],form['curiosidade'])
        
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

