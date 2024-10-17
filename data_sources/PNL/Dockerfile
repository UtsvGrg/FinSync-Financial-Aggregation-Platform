# Use a base image with Python
FROM python:3.9-slim

# Install necessary packages and clean up
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    pip install flask && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application files
COPY app.py init_db.py pnl.json ./

# Initialize the database
RUN python init_db.py

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
