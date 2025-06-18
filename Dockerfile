FROM python:3.10.8

WORKDIR /vpn

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./vpn/ /vpn/
