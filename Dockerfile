# ---- Build stage ----
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime stage ----
FROM python:3.10-slim

WORKDIR /app

# Create non-root user first
RUN useradd -m appuser

# Copy installed packages to appuser's home directory
COPY --from=builder /root/.local /home/appuser/.local
# Copy app code and templates
COPY app.py .
COPY templates/ ./templates/

# Update PATH for appuser
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Ensure ownership is given to appuser
RUN chown -R appuser:appuser /home/appuser /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]