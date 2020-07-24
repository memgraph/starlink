FROM python:3.7

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get --yes install cmake

# Install poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

# Install mgclient
RUN git clone https://github.com/memgraph/mgclient.git /mgclient && \
    cd mgclient && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

ENTRYPOINT [ "poetry", "run" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["python", "main.py", "start", "command"]