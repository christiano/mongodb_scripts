#!/usr/bin/env python

# Gera inserts randomicos
# Para testar sharding e shard-key
# Christiano Anderson


import pymongo
import random
import datetime


#cli.pybr.authenticate('user','pass')

def gera_nome():

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    pw_length = 16
    mypw = ""

    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]

    return(mypw)


ufs = ['AC','AP','AM','RO','PI','PE','CE','DF','RJ','SP','SC','RS','GO']
#ufs = ['PR']


while True:
    cli = pymongo.MongoClient('mongodb://endor.pybr.net:30011,endor.pybr.net:30012,endor.pybr.net:30013/?replicaSet=rs1')
    db = cli.escola
    #cli.escola.authenticate('escola','teste')
    cod = random.randint(1,9999999)
    nome = gera_nome()
    email = nome + "@email.fake"
    agora = datetime.datetime.now()
    db.cadastro.insert({
        'cod': cod,
        'nome': nome,
        'email': email,
        'uf': random.choice(ufs),
        'data_cadastro': agora})

    print nome
    cli.close()
