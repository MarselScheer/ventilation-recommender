SHELL := /bin/bash
.ONESHELL:
REPO_NAME := $(shell basename $$PWD)
IDE_CONTAINER := ventilation-ide

-include .env

build-docker-ide:
	@echo -------------------- $@ $$(date) --------------------
	-rm -rf docker_context
	mkdir docker_context
	cp iac/ide/* docker_context
	sudo docker build \
	  -t $(REPO_NAME)-ide:latest \
	  docker_context

start-docker-ide:
	@echo -------------------- $@ $$(date) --------------------
	sudo docker run -i -t --rm \
	  -v ~/docker_fs:/tmp/hostfs \
	  -v /home/m/docker_fs/dots/.ssh:/home/m/.ssh \
	  -v /tmp/.X11-unix:/tmp/.X11-unix \
	  -p 8000:8000 \
	  --name $(IDE_CONTAINER) \
	  $(REPO_NAME)-ide:latest


start-dashboard:
	@echo -------------------- $@ $$(date) --------------------
	sudo docker run \
	  --rm \
	  -d \
	  -v /data:/data \
	  -p 8000:8000 \
	  marselscheer/ventilation-dashboard:20240926

app-build:
	@echo -------------------- $@ $$(date) --------------------
	-rm -rf docker_context
	mkdir docker_context
	cp iac/app/* docker_context
	cp Makefile docker_context
	cp -r src docker_context
	cp -r .streamlit docker_context
	sudo docker build \
	  -t $(REPO_NAME):latest \
	  docker_context

venv:
	@echo -------------------- $@ $$(date) --------------------
	python -m venv venv
	source venv/bin/activate
	pip install shiny==1.1.0 matplotlib==3.2.9

run-dashboard-in-dev-mode: venv
	@echo -------------------- $@ $$(date) --------------------
	source venv/bin/activate
	shiny run src/app.py --host 0.0.0.0 --port 8000 --reload

run-app-in-dev-mode: venv
	@echo -------------------- $@ $$(date) --------------------
	source venv/bin/activate
	export DEVELOPMENT=True
	export PUSHBULLET_TOKEN=$(PUSHBULLET_TOKEN)
	rm /tmp/monitor.log
	make run-app

list-shortcomings:
	@echo -------------------- $@ $$(date) --------------------
	fgrep ";;s" README.org | sort -r | fgrep "||$(rate)"
