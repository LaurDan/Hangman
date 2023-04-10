FROM python:3.10-alpine AS builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk add gcc libc-dev libffi-dev
RUN pip install --upgrade pip
RUN pip3 install poetry==1.2.1

WORKDIR /new_app
COPY alembic.ini poetry.lock pyproject.toml .env.testing /new_app/

RUN mkdir /new_app/migrations
COPY /migrations/ /new_app/migrations/

RUN mkdir /new_app/updateservice && touch /new_app/updateservice/app.py && poetry build -f wheel
COPY ./updateservice /new_app/updateservice

FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY --from=builder /new_app /app/

RUN pip3 install poetry==1.2.1
RUN poetry install

COPY --from=builder /new_app/dist/updateservice*.whl /app/
RUN pip3 install updateservice*.whl

EXPOSE 8080
CMD ["uvicorn", "updateservice.app:app", "--host", "0.0.0.0", "--port", "8080"]
