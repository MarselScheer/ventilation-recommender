FROM python:3.11.10-slim-bullseye

RUN apt update && apt install -y vim
COPY req.txt .
RUN pip install -r req.txt
COPY . .
EXPOSE 8000
CMD /entrypoint.sh
