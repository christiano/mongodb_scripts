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

    db = cli['company']

    doc = {
        '_id': cod,
        'name': fake.name(),
        'email': fake.email(),
        'birth': fake.date_time_between(start_date="-30y", end_date="now", tzinfo=None),
        'addresses': [
            {
                'type': 'Home',
                'street': fake.street_name(),
                'number': fake.building_number(),
                'neighborhood': fake.bairro(),
                'city': fake.city(),
                'state': fake.estado_sigla(),
                'zipcode': fake.postcode(),
            },
            {
                'type': 'Office',
                'Position': fake.job(),
                'Office Name': fake.company(),
                'street': fake.street_name(),
                'number': fake.building_number(),
                'neighborhood': fake.bairro(),
                'city': fake.city(),
                'state': fake.estado_sigla(),
                'zipcode': fake.postcode(),
            },

        ],
        'telephones': [
            {
                'type': 'Mobile',
                'number': fake.phone_number(),
            },
            {
                'type': 'Home',
                'number': fake.phone_number(),
            },
            {
                'type': 'Office',
                'number': fake.phone_number(),
            },

        ]
    }

    db.users.insert(doc)

    print doc['name']
