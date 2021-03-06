from flask import Flask, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

arq = './pessoas-front-end.db'
db = SqliteDatabase(arq)

class BaseModel(Model):
    class Meta:
        database = db

class Pessoa(BaseModel):
    nome = CharField()
    endereco = CharField()
    telefone = CharField()   

app = Flask(__name__)
db.connect()
db.create_tables([Pessoa])

@app.route("/")
def inicio():
    return "backend do sistema de pessoas; <a href=/listar_pessoas>API listar pessoas</a>"

@app.route("/listar_pessoas")
def listar_pessoas():
    # forma alternativa rápida: usando map (lambda)
    pessoas = list(map(model_to_dict, Pessoa.select()))
    return jsonify({'lista':pessoas})
    # referência: 
    # https://www.geeksforgeeks.org/python-map-function/
    
''' exemplo do map:

def dobrar(n):
    return n*2
numeros = [1, 2, 3]
resultado = map(dobrar, numeros)
print(resultado)
print(list(resultado))

execução:
<map object at 0x7ff0ca2d6a90>
[2, 4, 6]

'''


'''
exemplo de retorno:
{
  "lista": [
    {
      "endereco": "Casa 9", 
      "id": 1, 
      "nome": "Joao da Silva", 
      "telefone": "3541-1230"
    }, 
    {
      "endereco": "Casa 9", 
      "id": 2, 
      "nome": "Joao da Silva", 
      "telefone": "3541-1230"
    }
  ]
}
'''

app.run(debug=True,port=4999)