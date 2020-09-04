FROM python:3
ENV PYTHONUNBUFFERED 1
RUN pip install poetry
RUN mkdir /src
WORKDIR /src
COPY . /src/
RUN poetry install


