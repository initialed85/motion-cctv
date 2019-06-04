FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    autoconf automake pkgconf libtool libjpeg8-dev build-essential libzip-dev gettext libmicrohttpd-dev \
    libavformat-dev libavcodec-dev libavutil-dev libswscale-dev libavdevice-dev uuid-runtime

COPY motion /srv/motion

WORKDIR /srv/motion

RUN autoreconf -fiv

RUN ./configure --prefix=/

RUN make

RUN make install

COPY res/handle_event.sh /srv/handle_event.sh

RUN mkdir -p /srv/target_dir

VOLUME /etc/motion

VOLUME /srv/target_dir

EXPOSE 8080

EXPOSE 8081

COPY res/entrypoint.sh /srv/entrypoint.sh

RUN echo `uuidgen` > /srv/instance.uuid

CMD /srv/entrypoint.sh
