# take a short cut here in using the datascience-image because
# it already comes with some basic things like emacs,
# language server, git, ... installed
FROM marselscheer/datascience-ide:20230810

ARG PYTHON_VERSION="3.10.10"

RUN apt update && \
    apt install -y libbz2-dev libffi-dev libssl-dev libsqlite3-dev liblzma-dev libncurses5-dev libreadline-dev sudo rsync && \
    chmod 777 /etc/sudoers && \
    echo "m  ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chmod 440 /etc/sudoers

RUN useradd -m m
USER m
WORKDIR /home/m
ENV DISPLAY=:0
ENV PYTHONPATH=./src
RUN curl https://pyenv.run | bash \
    && echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc \
    && echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc \
    && echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile \
    && echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile \
    && echo 'eval "$(pyenv init -)"' >> ~/.profile \
    && mkdir -p /tmp/hostfs \
    && ln -s /tmp/hostfs \
    && ln -s /tmp/hostfs/dots/.emacs.d.lean .emacs.d \
    && ln -s /tmp/hostfs/.gitconfig 

RUN ~/.pyenv/bin/pyenv install ${PYTHON_VERSION} \
    && ~/.pyenv/bin/pyenv global ${PYTHON_VERSION}

RUN ~/.pyenv/shims/pip install black \
    && curl -sSL https://install.python-poetry.org | ~/.pyenv/shims/python3 -

EXPOSE 8000
CMD /bin/bash
