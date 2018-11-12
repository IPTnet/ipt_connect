FROM alpine

ADD entrypoint.sh /entrypoint.sh

RUN \
    chmod +x /entrypoint.sh && \
    apk add --update --no-cache python py-pip gettext && \
    pip install --upgrade pip && \
    pip install Django>=1.9 gunicorn && \
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/entrypoint.sh"]
