# ---- Build stage ----
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime stage ----
FROM python:3.12-slim

WORKDIR /app

# Create a non-root user to run the app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy installed packages from the builder stage
COPY --from=builder /root/.local /home/appuser/.local

COPY app.py .

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PORT=5000

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
