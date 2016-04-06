#!/bin/bash

PASSWORD=changeit
VALIDITY=36524

CLUSTER="$1"; shift
NODE="$1"; shift

if [ -z "$CLUSTER" ] || [ -z "$NODE" ]; then
	echo "Usage: gen_node.sh <cluster> <node>"
	exit 1
fi

rm -f "${NODE}.jks" "${NODE}.csr" "${NODE}.cert"

echo "* Generate node keystore and keypair"
keytool -keystore "${NODE}.jks" -storepass "${PASSWORD}" \
	-genkeypair -alias "${NODE}" -dname "O=${CLUSTER}, OU=${NODE}" \
	-keyalg RSA -keysize 4096 -keypass "${PASSWORD}" -validity "${VALIDITY}"

echo "* Import cluster certificate into node keystore"
keytool -keystore "${NODE}.jks" -storepass "${PASSWORD}" \
	-importcert -alias "${CLUSTER}" -file "${CLUSTER}.cert" -noprompt

echo "* Create node CSR"
keytool -keystore "${NODE}.jks" -storepass "${PASSWORD}" \
	-certreq -alias "${NODE}" -file "${NODE}.csr" -keypass "${PASSWORD}"

echo "* Sign node CSR with cluster certificate"
openssl x509 -req -CA "${CLUSTER}.cert" -CAkey "${CLUSTER}.key" \
	-in "${NODE}.csr" -out "${NODE}.cert" -CAcreateserial -days "${VALIDITY}"
rm "${NODE}.csr"

echo "* Import node certificate into node keystore"
keytool -keystore "${NODE}.jks" -storepass "${PASSWORD}" \
	-importcert -alias "${NODE}" -file "${NODE}.cert" -keypass "${PASSWORD}"

echo "* Display keystore"
keytool -keystore "${NODE}.jks" -storepass "${PASSWORD}" \
	-list -v
