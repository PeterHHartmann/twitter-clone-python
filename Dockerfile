FROM python:3.9-alpine

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev

ENV PYTHONUNBUFFERED=1
ADD app/requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app
COPY /app /app

#RUN touch /app/production.py

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
