# Intro

This is a proof of concept for a distributed builds app.

# Setup

## Vagrant/Ansible

    vagrant up
    ansible-playbook -i inventory.py playbooks/site.yml

# Test

    cd app

## Python

    apt-get install python-virtualenv python-dev libffi-dev libssl-dev
    virtualenv venv
    source venv/bin/activate
    pip install ansible pika cassandra-driver

## Unit tests

    python -m unittest discover tests/

## App components

### Worker

Processes build requests and publishes build events.

    python worker.py

## Logger

Logs all the build events into the database.

    python logger.py

## Run

Submits a build request and displays the build events from the remote worker.

    python run.py "find /proc"
    python run.py "docker run --rm ubuntu:trusty /bin/bash -c 'sudo apt-get update; sudo apt-get install -y wget'"

## Replay

Replays the build events for a build from the database.

    python replay.py python replay.py 397aa31a-fa7a-11e5-8812-5c514f640c0d
