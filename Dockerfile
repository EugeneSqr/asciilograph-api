FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update && \
    apt-get -y install gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get -y --purge autoremove gcc

CMD [ "uvicorn", "--factory", "main:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-exclude", "**/*.py", "--reload-include", "./touch_reload" ]
