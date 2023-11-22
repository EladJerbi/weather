# Use the official Python image as the base image
FROM docker.io/python:3.10

# Create a non-root user
RUN useradd -m weather

# Switch to the non-root user
USER weather

# Set the working directory in the container
WORKDIR /home/weather/weather-app

# Copy the current directory contents into the container at /weather-app
COPY . .

# Install any necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/home/weather:$PYTHONPATH

# Make the start.sh script executable
RUN chmod +x start.sh

# Expose the port that the application runs on
EXPOSE 80

# Define the command to run the application when the container starts
CMD ["./start.sh"]
