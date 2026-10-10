FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home --uid 1001 appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY generate_data.py .
USER appuser
CMD ["python", "generate_data.py"]
