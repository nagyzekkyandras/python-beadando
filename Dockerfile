FROM python:3.14-rc-slim

WORKDIR /app
COPY ./src/ /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y default-libmysqlclient-dev gcc pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
