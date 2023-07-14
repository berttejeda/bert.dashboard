ARG DEVOPS_CLI_IMAGE=berttejeda/devops-cli
ARG DEVOPS_CLI_IMAGE_VERSION=1.0.0

FROM node:16.5.0 AS assets

WORKDIR /setup

COPY --chown=node . .

ENV REACT_APP_VERSION=0.1
ENV REACT_DEFAULT_SITE_ID=bert.self
ENV REACT_DEFAULT_SITE_USER=Anonymous
ENV REACT_APP_API_HOST=http://127.0.0.1:10000
ENV REACT_APP_API_URI_GET_FOOTER=${REACT_APP_API_HOST}/api/getFooterWebSocketAddress
ENV REACT_APP_API_URI_GET_TOPICS=${REACT_APP_API_HOST}/api/getTopics
ENV REACT_APP_API_URI_GET_RIGHTPANE=${REACT_APP_API_HOST}/api/getRightPaneWebSocketAddress
ENV REACT_APP_API_URI_LOAD_LESSON=${REACT_APP_API_HOST}/api/loadLesson
ENV REACT_APP_API_URI_PING=${REACT_APP_API_HOST}/api/ping

RUN yarn install --network-timeout 1000000000
RUN yarn build

FROM $DEVOPS_CLI_IMAGE:$DEVOPS_CLI_IMAGE_VERSION

RUN sudo apt update 

RUN sudo apt install nginx -y

RUN sudo mkdir -p /var/log/nginx

WORKDIR /setup

ADD . .

COPY --from=assets /setup/dashboard.gui ./

RUN sudo pip install .

WORKDIR /app

RUN sudo rm -rf /setup

RUN mkdir etc

ADD etc/ etc/

ADD docker/entrypoint.sh /usr/local/bin

RUN sudo chmod +x /usr/local/bin/entrypoint.sh

ENV USER=bill
ENV GROUP=bill
ENV USERHOME=/home/$USER
ENV UID=6000
ENV USER_PYTHON_LOCAL=/opt/python/.local
ENV USER_PYTHON_LIB=$USER_PYTHON_LOCAL/lib
ENV USER_PYTHON_BIN=$USER_PYTHON_LOCAL/bin
ENV PATH="$USER_PYTHON_BIN:$PATH"

RUN echo "===> Creating service user ..."  &&\
sudo useradd -m -s /bin/bash -G sudo,docker --uid "$UID" "$USER"

USER $USER

WORKDIR $USERHOME

RUN mkdir ./.ssh

RUN echo "===> Generating ssh keys" &&\
ssh-keygen -f $USERHOME/.ssh/id_rsa -t rsa -N '' &&\
chmod 600 $USERHOME/.ssh/id_rsa &&\
chmod 644 $USERHOME/.ssh/id_rsa.pub

RUN ecli plugins.install -R -r https://github.com/berttejeda/bert.dashboard.plugins.git

ENTRYPOINT [ "entrypoint.sh" ]