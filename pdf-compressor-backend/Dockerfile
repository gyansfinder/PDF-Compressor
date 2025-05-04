# Use an official Python image
FROM python:3.10-slim

# Install Ghostscript
RUN apt-get update && apt-get install -y ghostscript

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (match the port your Flask app runs on)
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
