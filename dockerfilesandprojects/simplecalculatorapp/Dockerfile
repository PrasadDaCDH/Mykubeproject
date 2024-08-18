FROM ubuntu

#need to install python first
RUN apt-get update && apt-get install -y python3

WORKDIR /app

COPY . /app

#Command to start the app
CMD ["python3", "calculator.py"]
 
