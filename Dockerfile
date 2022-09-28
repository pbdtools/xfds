FROM fnndsc/python-poetry:1.1.13

WORKDIR /docs

EXPOSE 8000

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry install

COPY . .
