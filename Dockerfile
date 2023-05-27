FROM python:3.11.3

ENV PYTHONUNBUFFERED 1

WORKDIR /
EXPOSE 8080

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY ./app /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0" , "--reload" , "--port", "8080"]
