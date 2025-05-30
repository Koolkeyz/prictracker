FROM python:3.12

WORKDIR /app


COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade /app/pyproject.toml

COPY ./src /app/src

CMD ["fastapi", "run", "src/main.py", "--port", "80"]