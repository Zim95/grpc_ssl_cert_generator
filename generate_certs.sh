#!/bin/bash

# Define the directory for certificates
cert_dir="cert"

# Create the cert directory if it doesn't exist
mkdir -p "$cert_dir"

# Move to the cert directory
cd "$cert_dir" || exit

# Remove previously generated files if they exist
rm -f ca.crt ca.key server.csr server.key server.crt client.csr client.key client.crt ca.srl

# Generate the CA key and certificate
openssl req -new -x509 -days 365 -nodes -out ca.crt -keyout ca.key -subj "/CN=grpc_ca"

# Generate the server key and certificate
openssl req -new -nodes -out server.csr -keyout server.key -subj "/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# Generate the client key and certificate
openssl req -new -nodes -out client.csr -keyout client.key -subj "/CN=client"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365

# Cleanup
rm -f server.csr client.csr

echo "Certificates generated successfully in $cert_dir directory."
