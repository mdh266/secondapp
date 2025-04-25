FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml /app

RUN mkdir /app/pages && \
    pip install . --no-cache

COPY pages/about.py /app/pages/
COPY main.py /app
COPY entrypoint.sh /app

RUN chmod +x /app/entrypoint.sh
RUN pip install . --no-cache

EXPOSE 8501

ENTRYPOINT ["/app/entrypoint.sh"]
