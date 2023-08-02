
FROM python:3.9
COPY . /user/app 

WORKDIR /user/app
COPY . .

# install dependencies  
RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install cron
RUN pip install -r requirements.txt 


EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]             # must be JSON-array syntax
CMD ["./manage.py", "runserver", "0.0.0.0:8080"]

# CMD python manage.py crontab add &&\
#  python manage.py crontab show &&\
#  python manage.py makemigrations &&\
#  python manage.py migrate &&\
#  python manage.py runserver 0.0.0.0:8000
