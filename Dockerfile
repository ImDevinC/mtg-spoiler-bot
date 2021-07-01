FROM python:3.7-slim as pipenv

RUN pip install pipenv

COPY ./ ./tmp

RUN cd /tmp && pipenv lock --requirements > requirements.txt

FROM python:3.7-slim

WORKDIR /usr/src/app

COPY --from=pipenv /tmp/requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT "python"

CMD "main.py"

