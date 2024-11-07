# Use the official Python image with the desired version
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Add a health check to ensure the application is running
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000 || exit 1

# Define default command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
