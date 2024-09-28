FROM python:3.11.10-slim-bullseye

RUN apt update && apt install -y vim build-essential ninja-build zlib1g-dev libjpeg-dev
COPY req.txt .
RUN pip install -r req.txt
COPY . .
EXPOSE 8000
CMD /entrypoint.sh
