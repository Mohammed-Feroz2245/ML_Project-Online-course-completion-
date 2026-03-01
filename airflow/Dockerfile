FROM apache/airflow:2.9.1

# Switch to root to ensure permissions if needed
USER root

# We need to copy requirements from the parent directory
# Note: Docker build context is usually the folder the Dockerfile is in.
COPY ../requirements.txt /requirements.txt

USER airflow
RUN pip install --no-cache-dir -r /requirements.txt