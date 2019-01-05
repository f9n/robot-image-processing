#!/usr/bin/env bash

function clean_up() {
  apt-get purge wolfram-engine -y
  apt-get purge libreoffice* -y
  apt-get clean
  apt-get autoremove
}

function upgrade() {
  apt-get update
  apt-get dist-upgrade -y
  apt-get upgrade -y
}

function install_opencv() {
  pip3 install --user opencv-python
}

function install_docker() {
  curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
  usermod -aG docker pi
}
