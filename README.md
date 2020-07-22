starlink_simulator
===

## 1. Local

### 1.1. Install

Make sure you have `poetry` installed. Perform a full, local install:

```shell
make install    # runs: poetry install
```

### 1.2. Tests

Runs tests, all by default and generates code coverage report

```shell
make test       # runs all tests and flake8 linters
```

### 1.3. Run

Run 

```shell
poetry run python main.py hello <name>
```

## 2. Docker

### 2.1. Build

Build docker image with following command:

```shell
docker build -t starlink_simulator .

# If using docker-compose
docker-compose build
```

### 2.2. Tests

If you have Memgraph already running you can run tests from application Docker only:

```shell
docker run --rm -e MG_HOST=<host> -e MG_PORT=<port> starlink_simulator python -m pytest
```

If you want to run a full setup of Memgraph database and the application, use docker compose instead:

```shell
docker-compose run starlink_simulator python -m pytest
```

### 2.3. Run

Run docker container with custom arguments:

```shell
docker run --rm -p 3000:3000 starlink_simulator python main.py
```

In order to run full setup: Memgraph database and application, use docker compose instead:

```shell
# Make sure to run `docker-compose build` beforehand
docker-compose up

# The app will be listening on port 5100
curl http://localhost:3000
```
