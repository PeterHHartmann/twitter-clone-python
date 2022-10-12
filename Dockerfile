FROM python:3.9-alpine

RUN apk add libffi-dev

ENV PYTHONUNBUFFERED=1
ADD requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app/
COPY . /app/

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
