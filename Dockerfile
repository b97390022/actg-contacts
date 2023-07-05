FROM python:3.11.3-slim-bullseye as base

ENV SOURCE_FOLDER  /actg-contacts
ENV PUBLIC_FOLDER  //192.168.5.20/Public
ENV TARGET_FOLDER  /mnt/Public

ARG SMB_USER
ARG SMB_PWD

WORKDIR "${SOURCE_FOLDER}"

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y samba-client samba-common nfs-common cifs-utils sudo \
    && rm -rf /var/lib/apt/lists/*

# mkdir of data src folder
RUN mkdir "${TARGET_FOLDER}" && echo "username=${SMB_USER}\npassword=${SMB_PWD}\n" > "${SOURCE_FOLDER}"/.smbcredentials && chmod 600 "${SOURCE_FOLDER}"/.smbcredentials \
    && echo "${PUBLIC_FOLDER} ${TARGET_FOLDER} cifs credentials=${SOURCE_FOLDER}/.smbcredentials,iocharset=utf8" > /etc/fstab

ADD requirements.txt "${SOURCE_FOLDER}"
RUN pip install -r requirements.txt

COPY . "${SOURCE_FOLDER}"

USER root

CMD mount -a && python -m src.main

#########################
FROM base as test

#layer test tools and assets on top as optional test stage
RUN apt-get update && apt-get install -y curl

#########################
FROM base as final

# this layer gets built by default unless you set target to test