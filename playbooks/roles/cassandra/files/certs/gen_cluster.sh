#!/bin/bash

PASSWORD=changeit
VALIDITY=36524

CLUSTER="$1"; shift

if [ -z "$CLUSTER" ]; then
	echo "Usage: gen_cluster.sh <cluster>"
	exit 1
fi

rm -f \
	"${CLUSTER}-key.pem" "${CLUSTER}-cert.pem" \
	"${CLUSTER}-cert.srl" "${CLUSTER}-truststore.jks"

echo "* Generate cluster key-certificate"
openssl req -x509 \
	-newkey rsa:4096 -subj "/O=${CLUSTER}" -days "${VALIDITY}" -nodes \
	-keyout "${CLUSTER}-key.pem" -out "${CLUSTER}-cert.pem"

echo "* Add cluster certificate to cluster Java truststore"
keytool \
	-importcert -alias "${CLUSTER}" -file "${CLUSTER}-cert.pem" -noprompt \
	-keystore "${CLUSTER}-truststore.jks" -storepass "${PASSWORD}"

echo "* Display cluster Java truststore"
keytool -list \
	-keystore "${CLUSTER}-truststore.jks" -storepass "${PASSWORD}"
