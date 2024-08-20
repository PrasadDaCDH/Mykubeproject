FROM ubuntu

#installing the dependancies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    && rm -rf /var/lib/apt/list/*

#setting working directory in the container
WORKDIR /app

#Create and activate vm for python
RUN python3 -m venv venv

#copping the requirements.txt into the container
COPY requirements.txt /app
COPY mini_python /app

#installing django in requirements.txt
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
RUN cd mini_python

# Set the PATH to use the virtual environment's binaries
ENV PATH="/app/venv/bin:$PATH"

#Expose the port for django app
EXPOSE 8000

#Running the django server
ENTRYPOINT ["python3"]
CMD ["manage.py","runserver","0.0.0.0:8000"]
