# Use a base image with Python
FROM python:3.9-slim

# Install necessary packages
RUN pip install flask

# Set the working directory
WORKDIR /app

# Copy the application files
COPY app.py /app/
COPY init_db.py /app/

# Initialize the database
RUN python init_db.py

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
