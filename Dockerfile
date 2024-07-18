# Use the official Python image from the Docker Hub
FROM python:3.12.4-bookworm

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY app.py .
COPY secret.py .

# Run the Python script
CMD ["python", "app.py"]
