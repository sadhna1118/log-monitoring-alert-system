FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p logs reports models dashboard/static dashboard/templates

# Expose dashboard port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///security_logs.db

# Run dashboard by default
CMD ["python", "src/dashboard.py"]