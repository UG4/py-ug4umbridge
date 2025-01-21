FROM ubuntu:latest

COPY cookie_server.py /

RUN apt update && \
    DEBIAN_FRONTEND="noninteractive" apt install -y python3-pip python3-venv && \
    python3 -m venv venv && \
    . venv/bin/activate && \
    pip install umbridge && \
    pip install ug4py-base

CMD . venv/bin/activate && python3 cookie_server.py
