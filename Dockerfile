FROM python:3.9.10

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt

CMD python api_yamdb/manage.py runserver 0.0.0.0:8080