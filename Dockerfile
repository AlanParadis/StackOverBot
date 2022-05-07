FROM python:3.9.12

# Make a directory for the application
WORKDIR /app

#install dependencies
#COPY requirements.txt .
RUN pip install -U git+https://github.com/Pycord-Development/pycord python-dotenv

#copy the application
COPY /app .

#run the application
ENTRYPOINT ["python", "StackOverBot.py"]