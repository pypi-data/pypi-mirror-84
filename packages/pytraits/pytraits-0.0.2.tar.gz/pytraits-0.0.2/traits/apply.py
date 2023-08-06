import yaml
import json
import jq

def read_template(template_yaml):
    template = None
    with open(template_yaml) as f:
        template = yaml.load(f, Loader=yaml.FullLoader)
    return template

def read_traits(traits_yaml):
    traits = None
    with open(traits_yaml) as f:
        traits = yaml.load(f, Loader=yaml.FullLoader)
    return traits

def find_key(obj, path):
    paths = path.split('.')
    paths.remove('')
    key = paths[-1]
    paths = paths[:-1]
    for path in paths:
        if isinstance(obj, dict):
            if path in obj:
                obj = obj[path]
        elif isinstance(obj, list):
            obj = obj[int(path)]
    if key not in obj:
        obj[key] = None
    return obj, key, obj[key]


def apply(traits, template, helpers):

    if traits['apply-for'] != template['kind']:
        print('traits apply-for not equl to template kind')
        return
    for trait in traits['rules']:
        obj, key, value = find_key(template, trait['path'])
        if trait['action'] == 'replace':
            obj[key] = trait['value']
        if trait['action'] == 'function':
            func = getattr(helpers, trait['value'])
            obj[key] = func(obj[key])
        if trait['action'] == 'concat':
            obj[key] = obj[key] + trait['value']
        if trait['action'] == 'extend':
            if not obj[key]:
                obj[key] = []
            obj[key].extend(trait['value'])
    return template

import click
import importlib


@click.command()
@click.argument('traits', type=click.Path(exists=True))
@click.argument('template', type=click.Path(exists=True))
@click.argument('helpers', default='traits.helpers')
def main(traits, template, helpers):
    """Simple program apply traits to your template"""
    traits = read_traits(traits)
    template = read_template(template)
    helpers = importlib.import_module(helpers)
    click.echo(json.dumps(apply(traits, template, helpers)))
    

