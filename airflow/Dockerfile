FROM apache/airflow:2.9.1

# The image defaults to 'airflow' user. 
# Only use 'USER root' if you need to install OS packages via apt-get.
# Since we only need pip packages, we stay as 'airflow'.

COPY requirements.txt /opt/airflow/requirements.txt

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt