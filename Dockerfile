# Use Ubuntu as base image
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && \
    apt-get install -y libpq-dev
RUN apt-get install -y \
    python3 \
    python3-pip \
    postgresql \
    postgresql-contrib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create PostgreSQL database and user
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE DATABASE alemeno;" && \
    psql --command "CREATE USER shubham WITH PASSWORD 'shubham';" && \
    psql --command "ALTER ROLE shubham SET client_encoding TO 'utf8';" && \
    psql --command "ALTER ROLE shubham SET default_transaction_isolation TO 'read committed';" && \
    psql --command "ALTER ROLE shubham SET timezone TO 'UTC';" && \
    psql --command "GRANT ALL PRIVILEGES ON DATABASE alemeno TO shubham;"

# Switch back to root user
USER root

# Set working directory
WORKDIR /app

# Copy Django project files to container
COPY . /app/

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 8000

#Run postgresql
RUN service postgresql start

# Run Django project
CMD ["python3", "manage.py", "runserver"]
