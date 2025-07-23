# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port that the app runs on
EXPOSE 8080

# Run the application using Gunicorn, a production-ready WSGI HTTP server
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app
