"""
This script generates certificates for SSL based communication
between GRPC Server and Client.

For any inquiries, these are the emails of the Authors:

-> Namah Shrestha: shresthanamah@gmail.com
"""

# built-ins
import os
import logging
import sys
import time
import base64

# third party
import kubernetes


# CONSTANTS
CERTS_LIST: list = [
    "ca.crt", "ca.key", "ca.srl",
    "server.csr", "server.key", "server.crt",
    "client.csr", "client.key", "client.crt",
]
CLEANUP_LIST: list = ["server.csr", "client.csr"]


# kubernetes client
kubernetes.config.load_incluster_config()
kcli: kubernetes.client.CoreV1Api = kubernetes.client.CoreV1Api()


# logging setup
logger: logging.Logger = logging.getLogger(__name__)  # create logger
stream_handler: logging.StreamHandler = logging.StreamHandler(stream=sys.stdout)  # create stream handler
formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # create formatter
stream_handler.setFormatter(formatter)  # set formatter for handler
logger.addHandler(hdlr=stream_handler)  # add handler
logger.setLevel(logging.DEBUG)  # add level


# ENVs
CERT_DIRECTORY: str = os.getenv("CERT_DIRECTORY", "./cert")
TIMEOUT: int = int(os.getenv("TIMEOUT", 365*24*60*60))  # 365 days
SECRET_NAME: str = os.getenv("SECRET_NAME", "grpc-certs")
NAMESPACE: str = os.getenv("NAMESPACE", "default")
logger.info(
    f"Environments => "
    f"CERT_DIRECTORY: {CERT_DIRECTORY}, "
    f"TIMEOUT: {TIMEOUT}, "
    f"SECRET_NAME: {SECRET_NAME}, "
    f"NAMESPACE: {NAMESPACE}"
)


def execute_command(command: str) -> None:
    """
    Execute the terminal command.
    :params:
        :command: str: Terminal Command.
    :returns: None

    Author: Namah Shrestha
    """
    try:
        logger.info(f"Executing command: {command}")
        os.system(command)
    except Exception as e:
        logger.error(f"Error while executing command: {e}")
        raise Exception(e)


def create_cert_directory(cert_directory: str) -> None:
    """
    Create the certificate directory if it does not exist.
    :params:
        :cert_directory: str: Certificate directory.
    :returns: None

    Author: Namah Shrestha
    """
    try:
        if not os.path.exists(cert_directory):
            os.makedirs(cert_directory)
        logger.info(f"Successfully created directory: {cert_directory}")
    except Exception as e:
        logger.error(f"Error while creating cert directory: {e}")
        raise Exception(e)


def remove_files(cert_directory: str, file_list: list) -> None:
    """
    Remove old certificates from directory.
    :params:
        :cert_directory: str: Certificate directory.
    :returns: None

    Author: Namah Shrestha
    """
    for file in file_list:
        fname: str = f"{cert_directory}/{file}"
        try:
            os.remove(fname)
            logger.info(f"{fname} removed!")
        except Exception:
            logger.error(f"{fname} not found!")
            continue


def create_ca(cert_directory: str, common_name: str) -> None:
    """
    Create the CA in the cert_directory.
    :params:
        :cert_directory: str: Certificate directory.
    :returns: None

    Author: Namah Shrestha
    """
    command: str = (
        f"openssl req -new -x509 -days 365 -nodes "
        f"-out {cert_directory}/ca.crt "
        f"-keyout {cert_directory}/ca.key "
        f"-subj '/CN={common_name}'"
    )
    try:
        execute_command(command)
    except Exception as e:
        logger.error(f"Error in creating CA: {e}")
        raise Exception(e)


def create_client_csr(cert_directory: str, common_name: str) -> None:
    """
    Create the Client Certificate Signing Request in the cert_directory.
    :params:
        :cert_directory: str: Certificate directory.
    :returns: None

    Author: Namah Shrestha
    """
    command: str = (
        f"openssl req -new -nodes "
        f"-out {cert_directory}/client.csr "
        f"-keyout {cert_directory}/client.key "
        f"-subj '/CN={common_name}'"
    )
    try:
        execute_command(command)
    except Exception as e:
        logger.error(f"Error in creating client CSR: {e}")
        raise Exception(e)


def create_client_cert(cert_directory: str, timeout: int) -> None:
    """
    Create the Client Certificate in the cert_directory.
    :params:
        :cert_directory: str: Certificate directory.
    :returns: None

    Author: Namah Shrestha
    """
    required_files: list = [
        f"{cert_directory}/client.csr",
        f"{cert_directory}/ca.crt",
        f"{cert_directory}/ca.key"
    ]
    for required_file in required_files:
        if not os.path.exists(required_file):
            raise Exception(f"{required_file} not found! Cannot create client cert!")
    command: str = (
        f"openssl x509 -req "
        f"-in {cert_directory}/client.csr "
        f"-CA {cert_directory}/ca.crt "
        f"-CAkey {cert_directory}/ca.key "
        f"-CAcreateserial -out {cert_directory}/client.crt "
        f"-days {timeout}"
    )
    try:
        execute_command(command)
    except Exception as e:
        logger.error(f"Error in creating client cert: {e}")
        raise Exception(e)


def create_server_csr(cert_directory: str, common_name: str) -> None:
    """
    Create the Server Certificate Signing Request in the cert_directory.
    :params:
        :cert_directory: str: Certificate directory.
    :returns: None

    Author: Namah Shrestha
    """
    command: str = (
        f"openssl req -new -nodes "
        f"-out {cert_directory}/server.csr "
        f"-keyout {cert_directory}/server.key "
        f"-subj '/CN={common_name}'"
    )
    try:
        execute_command(command)
    except Exception as e:
        logger.error(f"Error in creating server CSR: {e}")
        raise Exception(e)


def create_server_cert(cert_directory: str, timeout: int) -> None:
    """
    Create the Server Certificate in the cert_directory.
    :params:
        :cert_directory: str: Certificate directory.
    :returns: None

    Author: Namah Shrestha
    """
    required_files: list = [
        f"{cert_directory}/server.csr",
        f"{cert_directory}/ca.crt",
        f"{cert_directory}/ca.key"
    ]
    for required_file in required_files:
        if not os.path.exists(required_file):
            raise Exception(f"{required_file} not found! Cannot create server cert!")
    command: str = (
        f"openssl x509 -req "
        f"-in {cert_directory}/server.csr "
        f"-CA {cert_directory}/ca.crt "
        f"-CAkey {cert_directory}/ca.key "
        f"-CAcreateserial -out {cert_directory}/server.crt "
        f"-days {timeout}"
    )
    try:
        execute_command(command)
    except Exception as e:
        logger.error(f"Error in creating server cert: {e}")
        raise Exception(e)


def create_kubernetes_secrets(cert_directory: str, secret_name: str, namespace: str) -> None:
    """
    Create the kubernetes secrets using kubernetes client in cluster config.
    Replace the secret if it already exists.
    :params:
        :cert_directory: Certificate directory.
        :secret_name: The name of the secret.
        :namespace: The namespace where the secret is to be deployed.
    :returns: None

    Author: Namah Shrestha
    """
    def read_cert(cert_name: str) -> bytes:
        """
        Read certificate and return certificate in bytes.
        :params:
            :cert_name: str: The name of the certificate.
        :returns: The certificate data in bytes.

        Author: Namah Shrestha
        """
        try:
            with open(f"{cert_directory}/{cert_name}", "rb") as fr:
                data: bytes = fr.read()
            return data
        except FileNotFoundError as fnfe:
            logger.error(f"Cannot find certificate! {cert_name}")
            raise FileNotFoundError(fnfe)
    
    try:
        ca_crt: bytes = read_cert("ca.crt")
        server_crt: bytes = read_cert("server.crt")
        server_key: bytes = read_cert("server.key")
        client_crt: bytes = read_cert("client.crt")
        client_key: bytes = read_cert("client.key")
        secret: kubernetes.client.V1Secret = kubernetes.client.V1Secret(
            metadata=kubernetes.client.V1ObjectMeta(name=secret_name),
            data={
                "ca.crt": base64.b64encode(ca_crt).decode('utf-8'),
                "server.crt": base64.b64encode(server_crt).decode('utf-8'),
                "server.key": base64.b64encode(server_key).decode('utf-8'),
                "client.crt": base64.b64encode(client_crt).decode('utf-8'),
                "client.key": base64.b64encode(client_key).decode('utf-8')
            }
        )
        kcli.create_namespaced_secret(namespace=namespace, body=secret)
        logger.info(f"Secret {secret_name} created successfully.")
    except FileNotFoundError as fnfe:
        raise FileNotFoundError(fnfe)
    except kubernetes.client.rest.ApiException as kcrae:
        if kcrae.status == 409:  # conflict secret already exists
            kcli.replace_namespaced_secret(name=secret_name, namespace=namespace, body=secret)
            logger.info(f"Secret {secret_name} replaced successfully.")
        else:
            logger.info(f"Error in creating kubernetes secret! {kcrae}")
            raise


def remove_old_secrets(secret_name: str, namespace: str) -> None:
    """
    Remove old kubernetes secret certificates.
    :params:
        :secret_name: str: Name of the secret.
        :namespace: str: Kubernetes namespace.
    :returns: None

    Author: Namah Shrestha
    """
    try:
        kcli.delete_namespaced_secret(name=secret_name, namespace=namespace)
        logger.info(f"Secret {secret_name} deleted successfully.")
    except kubernetes.client.rest.ApiException as kcrae:
        if kcrae.status == 404:
            logger.info(f"Secret {secret_name} not found in namespace {namespace}.")
        else:
            logger.error(f"Error in removing old kubernetes secret! {kcrae}")
            raise


def main() -> None:
    """
    The main runner of the script.
    1. Create a cert directory if it does not exist.
    2. Remove old certificates.
    3. Create the CA.
    4. Create Client CSR.
    5. Create Client Cert.
    6. Create Server CSR.
    7. Create Server Cert.
    8. Remove unnecessary files.
    9. Remove old Kubernetes secrets.
    10. Create new Kubernetes secrets.

    Author: Namah Shrestha
    """
    try:
        create_cert_directory(cert_directory=CERT_DIRECTORY)
        remove_files(cert_directory=CERT_DIRECTORY, file_list=CERTS_LIST)
        create_ca(cert_directory=CERT_DIRECTORY, common_name="grpc_ca")
        create_client_csr(cert_directory=CERT_DIRECTORY, common_name="client")
        create_client_cert(cert_directory=CERT_DIRECTORY, timeout=TIMEOUT)
        create_server_csr(cert_directory=CERT_DIRECTORY, common_name="localhost")
        create_server_cert(cert_directory=CERT_DIRECTORY, timeout=TIMEOUT)
        remove_files(cert_directory=CERT_DIRECTORY, file_list=CLEANUP_LIST)
        remove_old_secrets(secret_name=SECRET_NAME, namespace=NAMESPACE)
        create_kubernetes_secrets(cert_directory=CERT_DIRECTORY, secret_name=SECRET_NAME, namespace=NAMESPACE)
    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(TIMEOUT)
