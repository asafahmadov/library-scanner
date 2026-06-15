# Hardened image — apPosture auto-fix.
# - modern, supported base (was python:3.4, EOL with 100s of CVEs)
# - no secret baked into a layer
# - runs as a non-root user
# - no SSH exposure
FROM python:3.12-slim

RUN pip install --no-cache-dir flask==2.3.3 requests==2.32.3

COPY . /app
WORKDIR /app

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["python", "app.py"]
