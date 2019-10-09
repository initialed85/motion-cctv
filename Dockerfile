FROM ubuntu:16.04

ENV TZ Australia/Perth

ENV TARGET_DIR /srv/target_dir

ENV OUTPUT_PATH /srv/root/

ENV BROWSE_URL_PREFIX /browse/

ENV WEB_USERNAME cctv

ENV WEB_PASSWORD cctv123!@#

ENV COUNTRY AU

ENV STATE Western Australia

ENV LOCALE Perth

ENV ORGANIZATION Home

ENV COMMON_NAME motion-cctv

RUN apt-get update && apt-get install -y \
    autoconf automake pkgconf libtool libjpeg8-dev build-essential libzip-dev gettext libmicrohttpd-dev \
    libavformat-dev libavcodec-dev libavutil-dev libswscale-dev libavdevice-dev git tzdata nginx supervisor \
    logrotate apache2-utils openssl autopoint

RUN dpkg-reconfigure -f noninteractive tzdata

COPY motion /srv/motion

WORKDIR /srv/motion

RUN autoreconf -fiv

RUN ./configure --prefix=/

RUN make

RUN make install

RUN mkdir -p /srv/target_dir

RUN cp -frv /etc/motion /srv/default_etc_motion

RUN groupadd syslog

RUN openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
    -subj "/C=${COUNTRY}/ST=${STATE}/L=${LOCALE}/O=${ORGANIZATION}/CN=${COMMON_NAME}" \
    -keyout /etc/ssl/private/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt

RUN useradd nginx

RUN htpasswd -c -b /srv/nginx.htpasswd ${WEB_USERNAME} ${WEB_PASSWORD}

RUN mkdir /srv/root

COPY res/config.py /srv/config.py

COPY res/event_parser.py /srv/event_parser.py

COPY res/event_parser_loop.py /srv/event_parser_loop.py

COPY res/motion-cctv.conf /etc/supervisor/conf.d/motion-cctv.conf

COPY res/nginx.conf /etc/nginx/nginx.conf

COPY res/index.html /srv/root/index.html

VOLUME /etc/motion

VOLUME /srv/target_dir

EXPOSE 80

EXPOSE 443

EXPOSE 8080

EXPOSE 8081

CMD supervisord -n -c /etc/supervisor/supervisord.conf
