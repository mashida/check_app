# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY pyproject.toml /code/
RUN pip install --upgrade pip
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

# Copy project
COPY . /code/

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy the startup script
COPY startup.sh /startup.sh

# Make the script executable
RUN chmod +x /startup.sh

# Set the startup script as the entrypoint
ENTRYPOINT ["/startup.sh"]
