# Use the official Python 3.10 image from the Docker hub
FROM python:3.10

# Set environment variables to prevent Python from buffering stdout and stdin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code into the container
# COPY . /app/

# Expose the port on which the bot will run
EXPOSE 3978

# Define the command to run the application
CMD ["python", "app.py"]
