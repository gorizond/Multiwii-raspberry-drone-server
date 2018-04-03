FROM arm32v6/alpine

WORKDIR /drone-server

RUN apk add --update python && \
	apk add --update --virtual .build-deps build-base py-pip python-dev git && \
	pip install --no-cache-dir git+https://github.com/alduxvm/pyMultiWii.git && \
	pip install --no-cache-dir pyserial gevent-websocket flask-socketio && \
	apk del .build-deps && \
	rm -rf /var/cache/apk/*

CMD python run.py

ADD ./ ./

#RUN cp pyMultiWii/pyMultiwii.py ./pyMultiwii.py

