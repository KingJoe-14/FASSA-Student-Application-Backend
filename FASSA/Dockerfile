FROM python:3.10-slim

# Prevents Python from buffering stdout/err
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Expose port for gunicorn (optional)
EXPOSE 8000

CMD ["gunicorn", "fassa.wsgi:application", "--bind", "0.0.0.0:8000"]
