#!/usr/bin/python

import sys
import yaml
import json

env_filename = 'environments/vagrant.yml'

# Tentatively load environment
try:
  environment = yaml.load(open(env_filename, 'r'))
except Exception, e:
  print >>sys.stderr, str(e)
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

# Add magic host
inventory['_meta']['hostvars']['localhost'] = {
  'ansible_connection': 'local',
}

# Add magic group with all hosts
inventory['vagrant'] = {}
inventory['vagrant']['hosts'] = environment['hosts'].keys() + ['localhost']

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
