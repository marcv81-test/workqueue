# Intro

This is a proof of concept for a distributed builds app.

# Setup

## RabbitMQ

    apt-get install rabbitmq-server

## Cassandra

    echo "deb http://www.apache.org/dist/cassandra/debian 33x main" > /etc/apt/sources.list.d/cassandra.list
    echo "deb-src http://www.apache.org/dist/cassandra/debian 33x main" >> /etc/apt/sources.list.d/cassandra.list
    gpg --keyserver pgp.mit.edu --recv-keys 749D6EEC0353B12C
    gpg --export --armor 749D6EEC0353B12C | apt-key add -
    apt-get update
    apt-get install cassandra
    cqlsh <cql/init.cql

## Python

    apt-get install python-virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install cassandra-driver pika

# Test

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
