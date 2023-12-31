FROM python:3.11-alpine

# Copy in requirements.txt first (for caching purposes)
COPY requirements.txt /app/requirements.txt

# Install all the requirements
RUN pip install -r /app/requirements.txt

# Copy everthing from . to /app inside the 'box'
COPY ./src/ /app/src/
WORKDIR /app

# How to run it when we start up the box?
#CMD ["gunicorn", "-b 0.0.0.0:5000", "-w 2", "main:app"]
RUN opentelemetry-bootstrap --action=install
CMD ["opentelemetry-instrument", "uvicorn",  "src.main:app", "--host", "0.0.0.0", "--port", "80"]
