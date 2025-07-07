FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y python3.11 python3-pip


WORKDIR /app/src/auth

COPY src /app/src
COPY setup.py requirements.txt /app/

ENV PYTHONPATH=/app/src

RUN pip3 install --upgrade pip && \
    pip3 install -r /app/requirements.txt

CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
