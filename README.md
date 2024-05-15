# grpc_ssl_cert_generator
Client and Server Certificate generation for GRPC communication.


# How to run
1. Supported only for UNIX terminals at the moment.
2. Clone the repository.
    ```
    git clone https://github.com/Zim95/grpc_ssl_cert_generator.git
    ```
3. Run the following command to generate the certificates:
    ```
    ./grpc_ssl_cert_generator/generate_certs.sh
    ```
    This will create a `cert` directory from where ever the `generate_certs.sh` is called and generate all the certificates there.
