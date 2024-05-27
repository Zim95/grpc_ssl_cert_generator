FROM python:3.11-slim

# Define default env variables
ENV CERT_DIRECTORY="./certs"
ENV NAMESPACE="default"
ENV SECRET_NAME="grpc_certs"
ENV TIMEOUT=31536000

# setup workdir
RUN mkdir app
COPY generate_certs.py app/
COPY requirements.txt app/
WORKDIR app

# install dependencies
RUN apt-get update && apt-get install -y build-essential
RUN pip install -r requirements.txt

CMD ["python", "generate_certs.py"]
