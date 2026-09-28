# ---------- Stage 1: builder ----------
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: final runtime image ----------
FROM python:3.12-slim
WORKDIR /app

# Create a non-root user
RUN useradd --create-home --uid 1001 appuser

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY main.py .

USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
