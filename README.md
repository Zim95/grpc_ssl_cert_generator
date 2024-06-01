## grpc_ssl_cert_generator
Client and Server Certificate generation for GRPC communication.

### How to run
1. Supported only for UNIX terminals at the moment.
2. Please make sure Docker and Kubernetes are installed and configured.
3. Clone the repository.
    ```
    git clone https://github.com/Zim95/grpc_ssl_cert_generator.git
    ```
4. Run this `make` command:
    ```
    make deploy
    ```
5. To stop/delete the pods and roles run this command:
    ```
    make teardown
    ```

### How to debug
1. Supported only for UNIX terminals at the moment.
2. Please make sure Docker and Kubernetes are installed and configured.
3. Clone the repository.
    ```
    git clone https://github.com/Zim95/grpc_ssl_cert_generator.git
    ```
4. Run this `make` command:
    ```
    make deploydebug
    ```
5. Exec into the pod:
    ```
    kubectl exec -it <podname> -n browseterm -- bash
    ```
6. You can edit the file using `vim` or run the file.
    ```
    python generate_certs.py
    ```
    OR
    ```
    vim generate_certs.py
    ```
7. To stop/delete the pods and roles run this command:
    ```
    make teardowndebug
    ```
