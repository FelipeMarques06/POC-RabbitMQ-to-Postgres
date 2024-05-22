FROM python:3.10-slim-buster

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements /app/requirements

RUN pip install --no-cache-dir -r /app/requirements/base.txt

COPY . /app

EXPOSE 80

ENV NAME World

CMD ["python", "consumer/consumer.py"]
