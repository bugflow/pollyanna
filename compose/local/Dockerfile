FROM python:3.8.5-alpine

# uvicorn/uvloop need make
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev make
RUN apk add gfortran py-pip build-base freetype-dev libpng-dev openblas-dev
RUN apk add zlib-dev jpeg-dev gcc musl-dev

# Ensure terminal output is sent directly to logs
ENV PYTHONBUFFERED 1

# Install requirements
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# the kludge...
COPY ./post_pip_install.sh /post_pip_install.sh
run /post_pip_install.sh

WORKDIR /app

# ENTRYPOINT ["/entrypoint"]
