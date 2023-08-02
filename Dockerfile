
FROM python:3.9
COPY . /user/app 

WORKDIR /user/app
COPY . .

# install dependencies  
RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install cron
RUN pip install -r requirements.txt 


EXPOSE 8000
ENTRYPOINT ["python3"] 
CMD ["manage.py", "makemigrations"] && ["manage.py", "migrate"] && ["manage.py", "runserver", "0.0.0.0:8000"]