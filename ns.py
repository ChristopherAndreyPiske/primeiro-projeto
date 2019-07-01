import os, datetime
from peewee import *


arq = 'desperdicio.db'

db = SqliteDatabase(arq)


class BaseModel(Model):
    class Meta:
        database = db

class Produto(BaseModel):
    descricao = CharField()
    def __str__(self):
        return self.descricao
    
class Desperdicio(BaseModel):
    produto = ForeignKeyField(Produto)
    quantidade = IntegerField()
    def __str__(self):
        return "Houve desperdicio de cerca de "+str(self.quantidade)+"%"+" de "+str(self.produto)

class Registro(BaseModel):
    data = DateField()
    desperdicios = ManyToManyField(Desperdicio)
    pessoas = IntegerField()
    def __str__(self):
        s = "Em: "+str(self.data) + " havia "+str(self.pessoas)+" pessoas: "
        for d in self.desperdicios:
            s += str(d)
        return s            

# teste das classes: inicializar BD ---------------------------------

# apagar arquivo de banco de dados, caso exista
if os.path.exists(arq):
    os.remove(arq)

# conectar-se ao BD e criar tabelas
db.connect()
db.create_tables([Produto, Desperdicio, Registro, Registro.desperdicios.get_through_model()])



portG = Produto.create(descricao = "Pizza portuguesa grande")
maioG = Produto.create(descricao = "Maionese grande")
reg1 = Registro.create(data = datetime.date(2019, 6, 29), pessoas = 3)
reg1.desperdicios.add(Desperdicio.create(produto = portG, quantidade = 25))
reg2 = Registro.create(data = datetime.date(2019, 6, 29), pessoas = 6)
reg2.desperdicios.add(Desperdicio.create(produto = maioG, quantidade = 20))


print(reg1)
print(reg2)