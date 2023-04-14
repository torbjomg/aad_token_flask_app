# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# dont write pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# dont buffer pythong logs
ENV PYTHONUNBUFFERED 1

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose the port the app will run on
EXPOSE 1234

# Start the Flask app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:1234", "app:app"]

