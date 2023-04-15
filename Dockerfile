# syntax=docker/dockerfile:1
FROM dorowu/ubuntu-desktop-lxde-vnc

# install some dependencies for netlogo model using java

ARG MODEL_NAME
ARG NETLOGO_VERSION=6.3.0
ARG NETLOGO_NAME=NetLogo-$NETLOGO_VERSION
ARG NETLOGO_URL=https://ccl.northwestern.edu/netlogo/$NETLOGO_VERSION/$NETLOGO_NAME-64.tgz

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DISPLAY=:1.0
    
RUN mkdir /home/netlogo \
 # use curl instead of wget
 && curl -O $NETLOGO_URL \
 && tar xzf $NETLOGO_NAME-64.tgz -C /home/netlogo --strip-components=1 \
 && rm $NETLOGO_NAME-64.tgz \
 && cp /home/netlogo/netlogo-headless.sh /home/netlogo/netlogo-headw.sh \
 && sed -i -e 's/org.nlogo.headless.Main/org.nlogo.app.App/g' /home/netlogo/netlogo-headw.sh \
 && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && apt-get update && apt-get install -y libxrender1 libxtst6 openjdk-17-jdk

COPY . /home/

RUN apt-get update && apt-get install dos2unix && apt-get clean
RUN find /home/ -name *.sh | xargs dos2unix -b

RUN mv /home/src/Netlogo-Model/InfoDemo.nlogo /home/src/Netlogo-Model/NLModel.nlogo

# install the latest python version from Deadsnakes PPA
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.10 python3-pip

WORKDIR /home/src/Agent-Factory

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

