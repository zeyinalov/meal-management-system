# Use the official Python image with the desired version
FROM python:3.9-slim

# Update the package list and install git and other dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=production

# Expose port 5000
EXPOSE 5000

# Define the default command to run the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
