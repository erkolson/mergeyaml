import re
import sys
import oyaml as yaml
import collections
import click
from collections import OrderedDict
from meta import __version__

@click.command()
@click.version_option(__version__)
@click.option("-i", "--input", help="An input yaml file to merge.", multiple=True, type=click.File(mode='r'))
@click.option("-f", "--file", help="A file to merge, also used to write output.", type=click.File(mode='r+'))
@click.option("-o", "--output", help="An output file to use for writing merged yaml.", type=click.File(mode='w'))
@click.option("--set", help="A string representation of a dict to merge.", multiple=True)
def cli(file, input, set, output):
    result = OrderedDict()

    if file is not None:
        output = file
        fileyaml = yaml.safe_load(file)
        result = fileyaml

    for a_file in input:
        oneyaml = yaml.safe_load(a_file)
        result = deep_merge(result, oneyaml)

    for a_set in set:
        oneyaml = string_to_dict(a_set)
        result = deep_merge(result, oneyaml)

    if output is not None:
        output.seek(0)
        output.truncate()
        yaml.safe_dump(result, output, default_flow_style=False)
    else:
        yaml.safe_dump(result, sys.stdout, default_flow_style=False)

def string_to_dict(values):
    """
    Input string "web.image.tag=1.0.4" becomes a dict:
    { "web": { "image": { "tag": "1.0.4"}}}
    :param value: a string representation of a multi-level dict
    :return: dict
    """
    out = OrderedDict()
    for value in values.split(','):
        current_dict = OrderedDict()
        k,v = value.split("=", 1)
        if re.search(r'\.', k):
            temp = k.split('.')
            temp.append(v)
            current_dict = reduce(lambda x,y: {y: x}, temp[::-1])
        else:
            current_dict[k] = v
        out = deep_merge(out, current_dict)
    return out

# This one might be better to use:
# https://www.electricmonk.nl/log/2017/05/07/merging-two-python-dictionaries-by-deep-updating/
def deep_merge(dict1, dict2):
    """
    Recursively merge two dicts
    :param dict1: first dict
    :param dict2: second dict
    :return: OrderedDict
    """
    result = OrderedDict(dict1)
    for k,v in dict2.iteritems():
        if (k in result and isinstance(result[k], dict) and isinstance(dict2[k], collections.Mapping)):
            result[k] = deep_merge(result[k], dict2[k])
        else:
            result[k] = dict2[k]
    return result

if __name__ == "__main__":

    file = "test.yaml"
    set_string1 = "web.image.tag=1.0.4"
    set_string2 = "web.image.tag=1.0.4,web.image.repository=erikolson/env-test-error"
    new_dict1 = string_to_dict(set_string1)
    print new_dict1
    new_dict2 = multi_string_to_dict(set_string2)

    values = yaml.safe_load(open(file))

    deep_merge(values, new_dict2)

    yaml.safe_dump(values, sys.stdout, default_flow_style=False)
