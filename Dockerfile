FROM docker.io/library/python:3.12-alpine

WORKDIR /usr/src/app
COPY ./libreria/requirements.txt .
RUN pip install --no-cache -r ./requirements.txt && pip install gunicorn

COPY . .

CMD ["sh", "/usr/src/app/entrypoint.sh"]