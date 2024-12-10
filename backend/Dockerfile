# Use the official Python image
FROM python:3.14-slim

# Set the working directory
WORKDIR /app

# Copy requirements to the working directory
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files to the working directory
COPY . /app/

# Expose the port (Django typically runs on port 8000)
EXPOSE 8000

# Run the ASGI application for WebSocket support using Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "smartbuilding.asgi:application"]
