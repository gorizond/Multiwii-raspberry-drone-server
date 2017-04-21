FROM hypriot/rpi-alpine-scratch

RUN apk add --update python && \
	apk add --update --virtual .build-deps build-base py-pip python-dev && \
	pip install tornado pyserial RPi.GPIO && \
	apk del .build-deps && \
	rm -rf /var/cache/apk/*

WORKDIR /Multiwii-raspberry-drone-server

ADD ./ ./

CMD python main.py

