echo "BUILD START"
pip install --upgrade pip
pip3 install -r requirements.txt
apt-get install -y cron
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate 
python manage.py crontab add
python manage.py crontab show
echo "BUILD END"