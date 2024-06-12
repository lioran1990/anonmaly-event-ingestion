# Use the official PostgreSQL image as the base image
FROM postgres:13

# Set environment variables
ENV POSTGRES_DB mydb
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD pass

# Copy the initialization script into the container
COPY init-db.sh /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432