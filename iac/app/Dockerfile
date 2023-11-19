FROM python:3.10.10

RUN apt update && apt install -y vim
COPY req.txt .
RUN mkdir data && pip install -r req.txt
COPY . .
CMD make run-app
