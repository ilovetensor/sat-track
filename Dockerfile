FROM postgres
RUN PGPASSWORD=H6mD4KiJnnPJ6WxM6fp1OgUXoeZigxEI psql -h dpg-cj4uhdpitvpc73f464qg-a.oregon-postgres.render.com -U satellite_data_7tcv_user satellite_data_7tcv
COPY . /user/app 
WORKDIR /user/app


FROM python:3.9
COPY . /user/app 

WORKDIR /user/app
COPY . .

# install dependencies  
RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install cron
RUN pip install -r requirements.txt 


EXPOSE 8000

CMD ("python", "manage.py", "runserver")