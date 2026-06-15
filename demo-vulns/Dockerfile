# Intentionally misconfigured image (IaC + container demo target).
FROM python:3.4

# CWE-798: secret baked into the image layer.
ENV API_KEY="AKIAIOSFODNN7EXAMPLE"

RUN pip install flask==0.12.2 requests==2.19.1

COPY . /app
WORKDIR /app

# Runs as root, exposes SSH — CIS misconfigurations.
USER root
EXPOSE 22

CMD ["python", "app.py"]
