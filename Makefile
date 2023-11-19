SHELL := /bin/bash
.ONESHELL:
REPO_NAME := $(shell basename $$PWD)

app-build:
	@echo ----- $@ ----- $$(date)
	-rm -rf docker_context
	mkdir docker_context
	cp iac/app/* docker_context
	cp Makefile docker_context
	cp PUSHBULLET_TOKEN docker_context
	cp -r src docker_context
	cp -r .streamlit docker_context
	sudo docker build \
	  -t $(REPO_NAME):latest \
	  docker_context

ide-build:
	@echo ----- $@ ----- $$(date)
	-rm -rf docker_context
	mkdir docker_context
	cp iac/ide/* docker_context
	sudo docker build \
	  -t $(REPO_NAME)-ide:latest \
	  docker_context

ide-start:
	@echo ----- $@ ----- $$(date)
	sudo docker run -i -t --rm \
	  -v ~/docker_fs:/tmp/hostfs \
	  -v /tmp/.X11-unix:/tmp/.X11-unix \
	  -p 8501:8501 \
	  $(REPO_NAME)-ide:latest

venv:
	@echo ----- $@ ----- $$(date)
	python -m venv venv
	source venv/bin/activate
	pip install streamlit==1.28.2

~/.streamlit:
	@echo ----- $@ ----- $$(date)
	cp -r .streamlit ~

run-app: ~/.streamlit
	@echo ----- $@ ----- $$(date)
	source PUSHBULLET_TOKEN
	#streamlit run src/app.py &
	python src/measure.py

run-app-in-dev-mode: venv ~/.streamlit
	@echo ----- $@ ----- $$(date)
	source venv/bin/activate
	export DEVELOPMENT=True
	make run-app
