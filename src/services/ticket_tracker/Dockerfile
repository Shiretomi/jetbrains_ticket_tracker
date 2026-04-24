FROM python:3.11-slim as builder

WORKDIR /app

COPY ./src/services/ticket_tracker/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY ./config ./config

COPY ./src/common/utils ./utils

COPY ./src/services/ticket_tracker/ticket_tracker.py .

COPY ./src/services/ticket_tracker/components ./components

COPY ./src/common ./common

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

CMD ["python", "ticket_tracker.py"]