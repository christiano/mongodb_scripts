#!/usr/bin/env python3

import sys
import datetime
from pymongo import MongoClient

agora = datetime.datetime.now()

cli = MongoClient()

db = cli['escola']

def cadastro_aluno():
    print('** Cadastro de novo aluno **')
    cod = input('ID do Aluno: ')
    nome = input('Nome Completo: ')
    sala = input('Sala de Aula: ')

    col = db['alunos']

    res = col.insert_one({
        '_id': cod,
        'nome': nome,
        'sala': sala
    })

    return(res)

def cadastro_livro():
    print('** Cadastro de novo livro **')
    cod = input('Cod do Livro: ')
    titulo = input('Titulo do Livro: ')
    editora = input('Editora: ')

    col = db['livros']

    res = col.insert_one({
        '_id': cod,
        'titulo': titulo,
        'editora': editora
    })

    return(res)

def consulta_todos_alunos():

    col = db['alunos']

    res = col.find({})

    for r in res:
        print('Cod: ', r['_id'], 'Nome: ', r['nome'], ' Sala: ', r['sala'])


def consulta_todos_livros():

    col = db['livros']

    res = col.find({})

    print("** Todos os livros da biblioteca e status de locacal **")

    for r in res:
        if 'aluguel' in r:
            status = 'Alugado'
        else:
            status = 'Disponivel'

        print('Cod: ', r['_id'], 'Titulo: ', r['titulo'], 'Status: ', status)

def aluguel_livro():

    col_livros = db['livros']
    col_alunos = db['alunos']

    print("** Aluguel de livros **")

    id_aluno = input('Selecione o ID do Aluno: ')

    aluno = col_alunos.find_one({'_id': id_aluno})

    print("Livros disponiveis para o aluno ", aluno['nome'])

    livros_disponiveis = col_livros.find({'aluguel': {'$exists': False}})

    for l in livros_disponiveis:
        print(l['_id'], ' - ', l['titulo'])

    escolha = input('Escolha o ID do Livro que o aluno deseja alugar: ')

    atualiza_livro = col_livros.update_one({'_id': escolha},{'$set': {'aluguel': {'aluno_id': aluno['_id'], 'data_hora': agora}}})

    print("O livro foi alugado para o aluno")

def devolucao_livro():

    col_livros = db['livros']

    todos_alugados = col_livros.find({'aluguel': {'$exists': True}})

    print("** Os seguintes livros estao alugados: ")
    for x in todos_alugados:
        print(x['_id'], x['titulo'])

    devolucao = input('Escolha o ID do livro que sera devolvido: ')

    livro_dev = col_livros.find_one({'_id': devolucao})
    aluguel = livro_dev['aluguel']

    alteracao = col_livros.update_one({'_id': devolucao},{'$addToSet':{'historico_alugel': aluguel}})
    remocao = col_livros.update_one({'_id': devolucao},{'$unset':{'aluguel':True}})

    print('Livro devolvido com sucesso!')

def consulta_historico_locacao():

    col_livros = db['livros']

    livros = col_livros.find({'historico_alugel': {'$exists': True}})

    for l in livros:
        print(l['titulo'])
        print('Alugado ' + str(len(l['historico_alugel'])) + ' vezes.')
        for h in l['historico_alugel']:
            print('Aluno: ', h['aluno_id'], 'Data: ', h['data_hora'])
        print('***********')

print("""
*** Bem-vindo ao sistema de Escola ***

Escolha um item:

1 - Cadastro de novo Aluno
2 - Cadastro de novo Livro
3 - Consulta todos os Alunos
4 - Consulta todos os Livros
5 - Aluguel de Livro
6 - Devolucao de Livro
7 - Consulta historico de Locacao por Livro

""")

opcao = input('Escolha: ')

if opcao == '1':
    cadastro_aluno()
elif opcao == '2':
    cadastro_livro()
elif opcao == '3':
    consulta_todos_alunos()
elif opcao == '4':
    consulta_todos_livros()
elif opcao == '5':
    aluguel_livro()
elif opcao == '6':
    devolucao_livro()
elif opcao == '7':
    consulta_historico_locacao()
