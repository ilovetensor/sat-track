echo "BUILD START"
set -o errexit
pip install --upgrade pip
pip3 install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate 
echo "BUILD END"