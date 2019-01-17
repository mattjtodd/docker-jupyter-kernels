FROM jupyter/minimal-notebook

# Stepup to root for installing jdk-11
USER root
RUN apt-get update \
  && apt-get install -y openjdk-11-jdk-headless \
  && apt-get clean

USER $NB_UID

# No digest supplied with the file :(
RUN wget https://github.com/SpencerPark/IJava/releases/download/v1.2.0/ijava-1.2.0.zip && \
  unzip ijava-1.2.0.zip && \
  python3 install.py --sys-prefix && \
  jupyter kernelspec list && \
  rm -fr ijava-1.2.0.zip install.py java
