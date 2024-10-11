# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the server code into the container
COPY ./server /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow external access
EXPOSE 5000

# Run the Flask app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]