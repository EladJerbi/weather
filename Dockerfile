# Use the official Python image as the base image
FROM python:3.10-slim

# Create a non-root user
RUN useradd -m weather

# Set the working directory in the container
WORKDIR /home/weather/weather-app

# Copy the current directory contents into the container at /weather-app
COPY . .

# Change ownership of the entire /home/weather directory to the weather user
RUN chown -R weather:weather /home/weather

# Install any necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt && \
    chmod +x start.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch to the non-root user
USER weather

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/home/weather/weather-app:$PYTHONPATH

# Run the unit tests
RUN python3 -m unittest discover -s tests

# remove the tests directory
RUN rm -rf tests

# Expose the port that the application runs on
EXPOSE 80

# Define the command to run the application when the container starts
CMD ["./start.sh"]
