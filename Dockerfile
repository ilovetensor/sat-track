FROM python:3.9
COPY . /user/app 

WORKDIR /user/app
COPY . .

# install dependencies  
RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install cron
RUN pip install -r requirements.txt 

RUN python manage.py collectstatic --no-input 
RUN python manage.py makemigrations --no-input
RUN manage.py migrate 
RUN manage.py crontab add
RUN manage.py crontab show

EXPOSE 8000

CMD ("python", "manage.py", "runserver")