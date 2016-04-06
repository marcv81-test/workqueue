#!/bin/bash

PASSWORD=changeit
VALIDITY=36524

CLUSTER="$1"; shift

if [ -z "$CLUSTER" ]; then
	echo "Usage: gen_cluster.sh <cluster>"
	exit 1
fi

rm -f "${CLUSTER}.*"

echo "* Generate cluster certificate"
openssl req -new -x509 \
	-newkey rsa:4096 -subj "/O=${CLUSTER}" -days "${VALIDITY}" -nodes \
	-keyout "${CLUSTER}.key" -out "${CLUSTER}.cert"

echo "* Display cluster certificate"
openssl x509 -in "${CLUSTER}.cert" -text -noout

echo "* Create cluster truststore and import cluster certificate"
keytool -keystore "${CLUSTER}.jks" -storepass "${PASSWORD}" \
	-importcert -alias "${CLUSTER}" -file "${CLUSTER}.cert" -noprompt

echo "* Display cluster truststore"
keytool -keystore "${CLUSTER}.jks" -storepass "${PASSWORD}" \
	-list -v
