# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies for OpenCV and docTR
# We include libgl1 and libglib2.0-0 to avoid "libGL.so.1" and "libglib-2.0.so.0" errors
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
