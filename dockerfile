FROM python:3.10

WORKDIR /code

RUN mkdir ./logs

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .