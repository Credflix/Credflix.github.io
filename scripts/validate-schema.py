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
    # Catégories mises à jour avec toutes les catégories
    network_names = next(parse_yaml('_data/Networking_Equipments.yml')).keys()
    security_names = next(parse_yaml('_data/Security_Devices.yml')).keys()
    infrastructure_names = next(parse_yaml('_data/IT_Infrastructures.yml')).keys()
    application_names = next(parse_yaml('_data/Software_Applications.yml')).keys()
    iot_names = next(parse_yaml('_data/IoT.yml')).keys()
    telecom_names = next(parse_yaml('_data/Telecommunications_VoIP.yml')).keys()

    return {
        "definitions": {
            'default_credentials': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'Username': {'type': 'string'},
                        'Password': {'type': 'string'},
                    },
                    'required': ['Username', 'Password'],
                    'additionalProperties': False
                },
                'minItems': 1
            },
            'references': {
                'type': 'array',
                'items': {'type': 'string'},
                'minItems': 1
            }
        },
        'type': 'object',
        'properties': {
            'label': {'type': 'string'},
            'description': {'type': 'string'},
            'default_credentials': {'$ref': '#/definitions/default_credentials'},
            'network': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(network_names)): {'type': 'array'}
                },
                'additionalProperties': False
            },
            'security': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(security_names)): {'type': 'array'}
                },
                'additionalProperties': False
            },
            'infrastructure': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(infrastructure_names)): {'type': 'array'}
                },
                'additionalProperties': False
            },
            'applications': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(application_names)): {'type': 'array'}
                },
                'additionalProperties': False
            },
            'iot': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(iot_names)): {'type': 'array'}
                },
                'additionalProperties': False
            },
            'telecom': {
                'type': 'array',
                "patternProperties": {
                    '^({})$'.format('|'.join(telecom_names)): {'type': 'array'}
                },
                'additionalProperties': False
            },
            'references': {'$ref': '#/definitions/references'}
        },
        'required': ['label', 'description', 'default_credentials', 'references'],
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
