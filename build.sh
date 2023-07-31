echo "BUILD START"
pip install --upgrade pip
pip3 install -r requirements.txt
python manage.py collectstatic

python manage.py migrate 
echo "BUILD END"