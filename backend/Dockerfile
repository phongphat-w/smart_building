# Use the official Python image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc

# Install dependencies for PyTorch and torchaudio
# RUN apt-get update && apt-get install -y build-essential libsndfile1

# Set the working directory
WORKDIR /app

# Copy the entire folder to the working directory
COPY ./backend/ /app/backend/
COPY ./smart_building/ /app/smart_building/
COPY ./manage.py /app/manage.py

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Expose the port (Django typically runs on port 8000)
EXPOSE 8000

# Run the ASGI application for WebSocket support using Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "smart_building.asgi:application"]
