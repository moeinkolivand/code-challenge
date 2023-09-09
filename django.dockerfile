
FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt .

RUN apt-get update
RUN apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt

COPY . .

RUN chmod +X start.sh

EXPOSE 8000

CMD ["bash", "start.sh"]