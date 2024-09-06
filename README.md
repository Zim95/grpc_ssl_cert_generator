## grpc_ssl_cert_generator
Client and Server Certificate generation for GRPC communication.
This code re-runs after the timeout. It deletes the old certificates and regenerates the certificates.

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
4. First get the image on your local docker:
    ```
    make builddebug
    ```
5. Run this `make` command:
    ```
    make deploydebug
    ```
6. Exec into the pod:
    ```
    kubectl exec -it <podname> -n browseterm -- bash
    ```
7. You can edit the file using `vim` or run the file.
    ```
    python generate_certs.py
    ```
    OR
    ```
    vim generate_certs.py
    ```
8. Once you run the file, follow the steps in `How to check if its working` section.
9. To stop/delete the pods and roles run this command:
    ```
    make teardowndebug
    ```

### How to check if its working
1. Check if the secrets are generated.
    ```
    kubectl get secrets -n browseterm
    ```

    You should see this:
    ```
    NAME         TYPE     DATA   AGE
    grpc-certs   Opaque   5      19s
    ```
2. You can also describe the secrets and see what files exist.
    ```
    kubectl describe secret grpc-certs -n browseterm
    ```

    You should see this:
    ```
    Name:         grpc-certs
    Namespace:    browseterm
    Labels:       <none>
    Annotations:  <none>

    Type:  Opaque

    Data
    ====
    ca.crt:      1107 bytes
    client.crt:  985 bytes
    client.key:  1704 bytes
    server.crt:  989 bytes
    server.key:  1704 bytes
    ```
