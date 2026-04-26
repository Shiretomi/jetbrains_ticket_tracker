FROM python:3.11-slim as builder

WORKDIR /app

COPY ./src/services/SLA_tracker/requirements.txt .

COPY ./requirements.txt ./requirements_common.txt

RUN pip install --user --no-cache-dir -r requirements.txt

RUN pip install --user --no-cache-dir -r requirements_common.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY ./config ./config

COPY ./src/services/SLA_tracker/SLA_tracking.py .

COPY ./src/common ./common

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

CMD ["python", "SLA_tracking.py"]