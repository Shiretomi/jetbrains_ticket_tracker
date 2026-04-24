FROM python:3.11-slim as builder

WORKDIR /app

COPY ./src/services/commands_handler/requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

RUN pip install --user --no-cache-dir ansible-core

FROM python:3.11-slim

RUN apt-get update && apt-get install -y openssh-client sshpass && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY ./config ./config

COPY ./src/services/commands_handler/commands ./commands

COPY ./src/services/commands_handler/main_bot.py .

COPY ./src/common ./common

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

CMD ["python", "main_bot.py"]