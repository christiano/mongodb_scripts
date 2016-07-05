#!/usr/bin/env python

# This script populates a MongoDB collections with fake users
# Based on Brazilian location
# Christiano Anderson
# Twitter: @dump
# Blog: http://christiano.me

import pymongo

from faker import Factory

fake = Factory.create('pt_BR')

for cod in range(0,10000):

    cli = pymongo.MongoClient()

    db = cli['empresa']

    doc = {
        '_id': cod,
        'nome': fake.name(),
        'email': fake.email(),
        'nascimento': fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None),
        'enderecos': [
            {
                'tipo': 'Residencial',
                'logradouro': fake.street_name(),
                'numero': fake.building_number(),
                'bairro': fake.bairro(),
                'cidade': fake.city(),
                'uf': fake.estado_sigla(),
                'cep': fake.postcode(),
            },
            {
                'tipo': 'Comercial',
                'cargo': fake.job(),
                'empresa': fake.company(),
                'logradouro': fake.street_name(),
                'numero': fake.building_number(),
                'bairro': fake.bairro(),
                'cidade': fake.city(),
                'uf': fake.estado_sigla(),
                'cep': fake.postcode(),
            },

        ],
        'telefones': [
            {
                'tipo': 'Celular',
                'numero': fake.phone_number(),
            },
            {
                'tipo': 'Residencial',
                'numero': fake.phone_number(),
            },
            {
                'tipo': 'Comercial',
                'number': fake.phone_number(),
            },

        ]
    }

    db.funcionarios.insert(doc)

    print doc['name']
