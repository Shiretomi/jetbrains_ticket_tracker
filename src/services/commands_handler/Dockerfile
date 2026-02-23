FROM python:3.11-slim as builder

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

RUN pip install --user --no-cache-dir ansible-core

FROM python:3.11-slim

RUN apt-get update && apt-get install -y openssh-client sshpass && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY ./commands ./commands

COPY ./ansible ./ansible

COPY ./main_bot.py .

COPY --from=common . ./common

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

CMD ["python", "main_bot.py"]