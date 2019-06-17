from flask import Flask,render_template,request,session,redirect
app= Flask(__name__)
from peewee import *


db = SqliteDatabase('lista_pessoa.db')

class Pessoa(Model):

    nome=CharField()
    idade=CharField()
    nascimento=CharField()
    cpf=CharField()

    class Meta:
        database=db

lista=[]

try:
        
    db.connect()
    db.create_tables([Pessoa]) 

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






@app.route("/addpessoa")
def caramba():
    return render_template("adicionarpessoa.html")





@app.route("/listapessoa_sem_add")
def caramb1():

    return render_template("listarpessoa.html", So_cara_foda= Pessoa.select())






@app.route("/listapessoa", methods=["POST"])
def caramb2():

    nome= request.form["Nome"]
    idade= request.form["Idade"]
    nasci= request.form["Nascimento"]
    cpf= request.form["Cpf"]
    val=0
    # comparar cpfs
    while val==0:
        for pessoa in lista:
            if cpf == pessoa.cpf:
                return render_template("erro_add_pessoa.html")
        val=1
        
    Pessoa.create(nome=nome,idade=idade,nascimento=nasci,cpf=cpf)
    return redirect( "/listapessoa_sem_add" )





@app.route("/deletepessoa")
def caramb3():

    cpf= request.args.get("Cpf")
    for pessoa in lista:
        if cpf== pessoa.cpf:
            lista.remove(pessoa)
    return render_template("mensagem.html")





@app.route("/form_alterar")
def caramb4():

    cpf= request.args.get("Cpf")
    for pessoa in lista:
        if cpf== pessoa.cpf:
            return render_template("form_alterar.html", pessoa=pessoa)






@app.route("/alterar_pessoa", methods=["POST"])
def caramb5():

    nome= request.form["Nome"]
    idade= request.form["Idade"]
    nasci= request.form["Nascimento"]
    cpf= request.form["Cpf"]
    pessoa_alterada= Pessoa(nome,idade,nasci,cpf)
    for pessoa in range(len(lista)):
        if cpf== lista[pessoa].cpf:
            lista[pessoa] = pessoa_alterada
            return render_template("pessoa_alterada.html")

app.config["SECRET_KEY"] = "54321"
app.run(debug=True)

