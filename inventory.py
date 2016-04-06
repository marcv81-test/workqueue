#!/usr/bin/python

import os
import sys
import yaml
import json

# Tentatively load environment
try:
  if 'ENVIRONMENT' not in os.environ:
    raise Exception('ENVIRONMENT is undefined')
  environment = yaml.load(open(os.environ.get('ENVIRONMENT'), 'r'))
except Exception, e:
  print >>sys.stderr, str(e)
  print >>sys.stderr, 'ENVIRONMENT must point to a valid environment definition file'
  exit(-1)

# Initialize empty inventory
inventory = { '_meta': { 'hostvars': {} } }

# Add hosts
for host, properties in environment['hosts'].iteritems():
  inventory['_meta']['hostvars'][host] = {
    'ansible_ssh_user': 'vagrant',
    'ansible_ssh_host': properties['ip'],
    'ansible_ssh_private_key_file': '.vagrant/machines/' + host + '/virtualbox/private_key',
    'ansible_ssh_common_args': '-o StrictHostKeyChecking=no',
    'ansible_become': 'yes',
  }

# Add magic group with all hosts
inventory['vagrant'] = {}
inventory['vagrant']['hosts'] = environment['hosts'].keys()

# Add other groups
if 'groups' in environment:
  for group, properties in environment['groups'].iteritems():
    inventory[group] = {}
    inventory[group]['hosts'] = []
    if 'hosts' in properties:
      inventory[group]['hosts'] = properties['hosts']
    if 'children' in properties:
      inventory[group]['children'] = properties['children']

# Output inventory
print json.dumps(inventory)
