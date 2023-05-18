# Vehicle VIN locator

An implementation of a FastAPI backend to decode VINs, powered by the vPIC API and backed by a SQLite cache.

Note: (about soft delete)

## Development Requirements

- Python >= 3.10
- Pip
- Poetry (Python Package Manager)


## Installation

```sh
python -m venv venv
source venv/bin/activate
make install
```

## Runnning Localhost

`make run`

## Deploy app

`make deploy`

## Running Tests

`make test`

## Access Swagger Documentation

> <http://localhost:8080/docs>


## Project structure

Files related to application are in the `app` or `tests` directories.
Application parts are:

   app                 # Fast-API stuff
    |
    | 
    ├── api                 - web routes
    ├── core                - application configuration, startup events, logging.
    ├── models              - pydantic models for this application.
    ├── services            - logic that is not just crud related.
    ├── main.py             - FastAPI application creation and configuration.
    │
   tests               # Pytest stuff
│     └── test_*            - unittest.
