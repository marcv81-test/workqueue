#!/bin/bash

PASSWORD=changeit
VALIDITY=36524

CLUSTER="$1"; shift
NODE="$1"; shift

if [ -z "$CLUSTER" ] || [ -z "$NODE" ]; then
	echo "Usage: gen_node.sh <cluster> <node>"
	exit 1
fi

rm -f \
	"${NODE}-key.pem" "${NODE}-cert.pem" \
	"${NODE}.pkcs12" "${NODE}-keystore.jks"

echo "* Generate node key and certificate request"
openssl req \
	-newkey rsa:4096 -subj "/O=${CLUSTER}/OU=${NODE}" -nodes \
	-keyout "${NODE}-key.pem" -out "${NODE}-req.pem"

echo "* Sign node certificate request with cluster key-certificate"
openssl x509 \
	-CA "${CLUSTER}-cert.pem" -CAkey "${CLUSTER}-key.pem" -CAcreateserial \
	-req -in "${NODE}-req.pem" -out "${NODE}-cert.pem" -days "${VALIDITY}"
rm "${NODE}-req.pem"

echo "* Package node PKCS12 key-certificate"
openssl pkcs12 -export \
	-name "${NODE}" -in "${NODE}-cert.pem" -inkey "${NODE}-key.pem" \
	-out "${NODE}.pkcs12" -passout pass:

echo "* Add node PKCS12 key-certificate to node Java keystore"
keytool -importkeystore -alias "${NODE}" \
	-srckeystore "${NODE}.pkcs12" -srcstorepass "" -srcstoretype pkcs12 \
	-destkeystore "${NODE}-keystore.jks" -deststorepass "${PASSWORD}"

echo "* Add cluster certificate to node Java keystore"
keytool \
	-importcert -alias "${CLUSTER}" -file "${CLUSTER}-cert.pem" -noprompt \
	-keystore "${NODE}-keystore.jks" -storepass "${PASSWORD}"

echo "* Display node Java keystore"
keytool -list \
	-keystore "${NODE}-keystore.jks" -storepass "${PASSWORD}"
