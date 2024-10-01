#!/usr/bin/env python3
import jsonschema
import os
import sys
import yaml

def parse_yaml(path):
    with open(path) as fs:
        text = fs.read()
        return yaml.load_all(text, Loader=yaml.SafeLoader)

def build_schema():
    # Catégories mises à jour avec seulement Network, Applications, et Databases
    network_names = next(parse_yaml('_data/network.yml')).keys()
    application_names = next(parse_yaml('_data/applications.yml')).keys()
    database_names = next(parse_yaml('_data/databases.yml')).keys()

    return {
        "definitions": {
            'examples': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'description': {'type': 'string'},
                        'code': {'type': 'string'},
                    },
                    'additionalProperties': False
                },
                'minimum': 1
            }
        },
        'type': 'object',
        'properties': {
            'description': {'type': 'string'},
            'command': {'type': 'string'},
            'network': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(network_names)): {'$ref': '#/definitions/examples'}
                },
                'additionalProperties': False
            },
            'applications': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(application_names)): {'$ref': '#/definitions/examples'}
                },
                'additionalProperties': False
            },
            'databases': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(database_names)): {'$ref': '#/definitions/examples'}
                },
                'additionalProperties': False
            },
            'references': {
                'type': 'array',
                'additionalProperties': False
            }
        },
        'required': ['network', 'applications', 'databases', 'references'],
        'additionalProperties': False
    }

def validate_directory(root):
    schema = build_schema()
    root, _, files = next(os.walk(root))
    for name in files:
        if not name.endswith('.md'):
            continue
        path = os.path.join(root, name)
        data = parse_yaml(path)
        try:
            jsonschema.validate(next(data), schema)
        except jsonschema.exceptions.ValidationError as err:
            print('{}: {}'.format(name, err))
            sys.exit(1)

if __name__ == '__main__':
   validate_directory("_credflix/") 
