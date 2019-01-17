FROM jupyter/minimal-notebook

USER root

RUN set -ex \
  && apt-get update \
  && apt-get install -y libtool libffi-dev ruby ruby-dev make libzmq3-dev libczmq-dev \
  && apt-get clean \
  && gem install cztop iruby \
  && iruby register --force

USER $NB_UID
