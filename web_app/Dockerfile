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
    git checkout 5ae69ea4774e9b525a2be0c9fc25fb83490f13bb && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

# Install dos2unix
RUN apt-get update && \
    apt-get install -y dos2unix

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app
EXPOSE 5000

ADD start.sh /
RUN chmod +x /start.sh
RUN dos2unix /start.sh

ENTRYPOINT [ "poetry", "run" ]
CMD ["/start.sh"]