"""
This script generates certificates for SSL based communication
between GRPC Server and Client.

For any inquiries, these are the emails of the Authors:

-> Namah Shrestha: shresthanamah@gmail.com
"""

# built-ins
import os


# CONSTANTS
CERT_DIRECTORY: str = "./cert"
CERTS_LIST: list = [
    "ca.crt", "ca.key", "ca.srl",
    "server.csr", "server.key", "server.crt",
    "client.csr", "client.key", "client.crt",
]
CLEANUP_LIST: list = ["server.csr", "client.csr"]
TIMEOUT: int = 365  # 365 days


def execute_command(command: str) -> None:
    """
    Execute the terminal command.
    :params:
        :command: str: Terminal Command.
    :returns: None

    Author: Namah Shrestha
    """
    try:
        os.system(command)
    except Exception as e:
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
    except Exception as e:
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
        except Exception:
            print(f"{fname} not found!")
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
        raise Exception(e)


def create_kubernetes_secrets() -> None:
    pass


def remove_old_secrets() -> None:
    """
    Remove old kubernetes secret certificates.

    Author: Namah Shrestha
    """
    pass


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
    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    main()

