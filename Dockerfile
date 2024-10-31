# lightweight base image
FROM python:3.9-slim-bullseye

# Set up a non-root user for security
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY QueueShield/ ./QueueShield/

# Set permissions and change ownership to non-root user
RUN chown -R appuser:appgroup /app
RUN chmod -R 755 /app

# Switch to the non-root user
USER appuser

# Define command to run the application
ENTRYPOINT ["python", "-m", "QueueShield.main"]
