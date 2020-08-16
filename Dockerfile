FROM python:3.8.1-alpine3.11

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN set -e; \
    apk add postgresql-dev gcc musl-dev --no-cache; \
    pip install pipenv; \
    pipenv install --ignore-pipfile --dev;

ENV PORT 8000

CMD [ "pipenv" , "run", "dev" ]

