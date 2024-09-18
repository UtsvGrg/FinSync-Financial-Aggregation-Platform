FROM python:3.9-slim

# Install necessary packages
RUN pip install flask

# Set the working directory
WORKDIR /app

# Copy the application files
COPY app.py /app/
COPY init_db.py /app/
COPY balance.json /app/

# Initialize the database
RUN python3 init_db.py

# Expose the port the app runs on
EXPOSE 5002

# Run the application
CMD ["python3", "app.py"]
