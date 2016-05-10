#!/bin/bash

VALIDITY=36524

CLUSTER="$1"; shift
PASSWORD="$1"; shift

if [ -z "$CLUSTER" ] || [ -z "$PASSWORD" ]; then
	echo "Usage: gen_cluster.sh <cluster> <password>"
	exit 1
fi

rm -rf ${CLUSTER}
mkdir ${CLUSTER}

echo "* Generate cluster key-certificate"
openssl req -x509 \
	-newkey rsa:4096 -subj "/O=${CLUSTER}" -days "${VALIDITY}" -nodes \
	-keyout "${CLUSTER}/cluster-key.pem" -out "${CLUSTER}/cluster-cert.pem"

echo "* Add cluster certificate to cluster Java truststore"
keytool \
	-importcert -alias "${CLUSTER}" -file "${CLUSTER}/cluster-cert.pem" -noprompt \
	-keystore "${CLUSTER}/cluster-truststore.jks" -storepass "${PASSWORD}"

echo "* Display cluster Java truststore"
keytool -list \
	-keystore "${CLUSTER}/cluster-truststore.jks" -storepass "${PASSWORD}"
