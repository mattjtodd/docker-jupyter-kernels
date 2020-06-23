FROM jupyter/minimal-notebook

# Stepup to root for installing jdk-11
USER root

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y \
      openjdk-11-jre-headless \
      ca-certificates-java && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# No digest supplied with the file :(
RUN wget https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip && \
  unzip ijava-1.3.0.zip && \
  python3 install.py --sys-prefix && \
  jupyter kernelspec list && \
  rm -fr ijava-1.3.0.zip install.py java
