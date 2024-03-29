FROM python:3.7

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install CMake for gqlalchemy
RUN apt-get update && \
  apt-get --yes install cmake && \
  rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

# Install dos2unix
RUN apt-get update && \
    apt-get install -y dos2unix

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY ./wait-for-it.sh /wait-for-it.sh 
RUN chmod +x /wait-for-it.sh
RUN dos2unix /wait-for-it.sh

COPY . /app

EXPOSE 3001

ENTRYPOINT [ "poetry", "run" ]