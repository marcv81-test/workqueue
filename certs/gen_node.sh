#!/bin/bash

PASSWORD=changeit
VALIDITY=36524

CLUSTER="$1"; shift
NODE="$1"; shift

if [ -z "$CLUSTER" ] || [ -z "$NODE" ]; then
	echo "Usage: gen_node.sh <cluster> <node>"
	exit 1
fi

if [ ! -d "$CLUSTER" ]; then
	echo "Please create cluster first"
	exit 1
fi

rm -f \
	"${CLUSTER}/${NODE}-key.pem" "${CLUSTER}/${NODE}-cert.pem" \
	"${CLUSTER}/${NODE}.pkcs12" "${CLUSTER}/${NODE}-keystore.jks"

echo "* Generate node key and certificate request"
openssl req \
	-newkey rsa:4096 -subj "/O=${CLUSTER}/OU=${NODE}" -nodes \
	-keyout "${CLUSTER}/${NODE}-key.pem" -out "${CLUSTER}/${NODE}-req.pem"

echo "* Sign node certificate request with cluster key-certificate"
openssl x509 \
	-CA "${CLUSTER}/cluster-cert.pem" -CAkey "${CLUSTER}/cluster-key.pem" -CAcreateserial \
	-req -in "${CLUSTER}/${NODE}-req.pem" -out "${CLUSTER}/${NODE}-cert.pem" -days "${VALIDITY}"
rm "${CLUSTER}/${NODE}-req.pem"

echo "* Package node PKCS12 key-certificate"
openssl pkcs12 -export \
	-in "${CLUSTER}/${NODE}-cert.pem" -inkey "${CLUSTER}/${NODE}-key.pem" \
	-name "${NODE}" -out "${CLUSTER}/${NODE}.pkcs12" -passout pass:"${PASSWORD}"

echo "* Add node PKCS12 key-certificate to node Java keystore"
keytool \
	-importkeystore -alias "${NODE}" \
	-srckeystore "${CLUSTER}/${NODE}.pkcs12" -srcstorepass "${PASSWORD}" -srcstoretype pkcs12 \
	-destkeystore "${CLUSTER}/${NODE}-keystore.jks" -deststorepass "${PASSWORD}"

echo "* Add cluster certificate to node Java keystore"
keytool \
	-importcert -alias "${CLUSTER}" -file "${CLUSTER}/cluster-cert.pem" -noprompt \
	-keystore "${CLUSTER}/${NODE}-keystore.jks" -storepass "${PASSWORD}"

echo "* Display node Java keystore"
keytool -list \
	-keystore "${CLUSTER}/${NODE}-keystore.jks" -storepass "${PASSWORD}"
