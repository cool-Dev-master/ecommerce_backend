py -m django startproject folder_name
    or
django-admin startproject folder_name
 
 
django-admin startapp app_name

python manage.py createsuperuser

python manage.py makemigrations

python manage.py migrate

python manage.py runserver


//To run Virtual env

pip install virtualenv

virtualenv -p python3 venv

venv\Scripts\activate

pip install -r requirements.txt

pip freeze > requirements.txt

to run : ./manage.py runserver


Here are some basic commands in Django that you might find useful:

Start a new Django project:
django-admin startproject project_name

Create a new Django app within a project:
python manage.py startapp app_name

Run the development server:
python manage.py runserver

Run database migrations:
python manage.py makemigrations
python manage.py migrate


Create a superuser for the admin interface:
python manage.py createsuperuser

Run tests:
python manage.py test

Generate Django documentation:
python manage.py doctext

Collect static files for deployment:
python manage.py collectstatic

Open Django shell:
python manage.py shell

Create a new Django app with tests:
python manage.py startapp --template=test-driven-app app_name


# Run the flush command to delete db all data
python manage.py flush

cd /path/to/your/project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
