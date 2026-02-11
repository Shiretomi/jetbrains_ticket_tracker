FROM python:3.11-slim as builder

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY ./utils ./utils

COPY ./ticket_tracker.py .

COPY --from=common . ./common

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

CMD ["python", "ticket_tracker.py"]