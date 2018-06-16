FROM arm32v6/alpine

WORKDIR /drone-server

RUN apk add --update python3 && \
	apk add --update --virtual .build-deps build-base py3-pip python3-dev git && \
	pip3 install --no-cache-dir git+https://github.com/wil3/pyMultiWii@feature-tcp && \
	pip3 install --no-cache-dir pyserial aiohttp && \
	apk del .build-deps && \
	rm -rf /var/cache/apk/*

CMD python run.py

ADD ./ ./
