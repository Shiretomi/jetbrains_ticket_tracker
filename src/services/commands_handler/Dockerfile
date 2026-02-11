FROM python:3.11-slim as builder

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY ./commands ./commands

COPY ./main_bot.py .

COPY --from=common . ./common

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

CMD ["python", "main_bot.py"]