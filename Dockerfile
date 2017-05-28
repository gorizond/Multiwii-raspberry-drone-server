FROM hypriot/rpi-alpine-scratch

WORKDIR /drone-server

RUN apk add --update python && \
	apk add --update --virtual .build-deps build-base py-pip python-dev git && \
	git clone https://github.com/alduxvm/pyMultiWii.git && \
	pip install pyserial gevent-websocket flask-socketio && \
	apk del .build-deps && \
	rm -rf /var/cache/apk/*


ADD ./ ./

RUN cp pyMultiWii/pyMultiwii.py ./pyMultiwii.py

CMD python run.py

