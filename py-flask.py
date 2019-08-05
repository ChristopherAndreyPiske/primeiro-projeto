from flask import Flask,render_template,request,session,redirect
app= Flask(__name__)
from peewee import *


db = SqliteDatabase('lista_pessoa.db')

class BaseModel(Model):
    class Meta:
        database=db

class Ingrediente(BaseModel):
    nome= CharField()
    valor= FloatField()

    def __str__(self):
        return self.nome + ", que custa: " + self.valor

class Receita(BaseModel):
    nome= CharField()

    def __str__(self):
        return self.nome + "é feito com: "

class Receita_ingrediente(BaseModel):
    receita= ForeignKeyField(Receita)
    ingrediente= ForeignKeyField(Ingrediente)
    quantidade= CharField()

    def __str__(self):
        return str(receita) + str(ingrediente) + "usando: " + self.quantidade

    def __str__(self):
        return self.nome + "que custa: " + self.valor

try:
        
    db.connect()
    db.create_tables([Ingrediente,Receita,Receita_ingrediente]) 

except OperationalError as e:
    print("erro ao criar tabelas: "+str(e))



@app.route("/")
def carai():
    return render_template("inicio.html")




@app.route("/login_form")
def cadas():
    return render_template("login.html")





@app.route("/login", methods=["POST"])
def cadas2():
    nome=request.form["Nome"]
    senha=request.form["Senha"]
    if nome=="Piske" and senha=="123":
        session["usuario"]=nome
        return redirect("/")
    else:
        return "sua senha ou/e nome podem estar ERRADOS"





@app.route("/logout")
def logout () :  
    session.pop("usuario") 
    return redirect("/")









@app.route("/addreceita")
def caramba2():
    return render_template("add_receita.html", lista_ingredientes= Ingrediente.select())


@app.route("/lista_receita", methods=["POST"])
def caramba3():

    nome= request.form["Nome"]
    ingrediente= request.form["Ingre"]
    quantidade= request.form["Quant"]
    
    val=0
    # comparar nomes
    while val==0:
        for ingre in Receita.select():
            if nome == ingre.nome:
                return render_template("erro_add_pessoa.html")
        val=1
    val=Receita.create(nome=nome)
    Receita_ingrediente.create(receita=val, ingrediente=Ingrediente.get_by_id(ingrediente), quantidade=quantidade)
    return redirect( "/" )


@app.route("/addingrediente")
def caramba():
    return render_template("add_ingrediente.html")


@app.route("/lista_ingre", methods=["POST"])
def caramb2():

    nome= request.form["Nome"]
    valor= request.form["Valor"]
    
    val=0
    # comparar nomes
    while val==0:
        for ingre in Ingrediente.select():
            if nome == ingre.nome:
                return render_template("erro_add_pessoa.html")
        val=1
        
    Ingrediente.create(nome=nome,valor=valor)
    return redirect( "/" )







@app.route("/lista_de_receitas")
def caramb1():

    return render_template("lista_receitas.html",receitas= Receita.select(),receita_ingredientes= Receita_ingrediente.select())




@app.route("/excluir receita")
def caramb3():

    nome = request.args.get("excluir receita")
    saia = Receita.select().where(Receita.nome == nome)
    saia_= Receita_ingrediente.select().where(Receita_ingrediente.receita == saia)
    for i in saia_:
        i.delete_instance()
    saia[0].delete_instance()
    return render_template("mensagem.html")





@app.route("/form_alterar")
def caramb4():

    cpf= request.args.get("Cpf")
    for pessoa in Pessoa.select():
        if cpf== pessoa.cpf:
            return render_template("form_alterar.html", pessoa=pessoa)






@app.route("/alterar_pessoa", methods=["POST"])
def caramb5():

    nome= request.form["Nome"]
    idade= request.form["Idade"]
    nasci= request.form["Nascimento"]

    saia = Pessoa.select().where(Pessoa.cpf == request.form["Cpf"])

    saia[0].nome=nome
    saia[0].idade=idade
    saia[0].nascimento=nasci
    saia[0].save()
    
    return render_template("pessoa_alterada.html")

app.config["SECRET_KEY"] = "54321"
app.run(debug=True)

