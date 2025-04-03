FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for SQLite database
RUN mkdir -p /app/data

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application using shell form to execute multiple commands
CMD python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000
