FROM python:3.12-slim

# Define the working directory
WORKDIR /app

# Install system dependencies required by systemd-python, pycairo and other Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    libcairo2-dev \
    pkg-config \
    libsystemd-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python requirements file into the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MarianaQuest.wsgi:application"]
