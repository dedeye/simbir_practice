FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /usercode
WORKDIR /usercode
COPY . /usercode/
RUN pip install -e .