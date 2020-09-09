FROM python:3.7

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app
EXPOSE 5000

ADD start.sh /
RUN chmod +x /start.sh

ENTRYPOINT [ "poetry", "run" ]
CMD ["/start.sh"]