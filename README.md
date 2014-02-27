Requirements
============
```
Django==1.6.2
PyYAML==3.10
South==0.8.4
argparse==1.2.1
psycopg2==2.5.2
wsgiref==0.1.2
```
Setup
=====

Create database user and database and fix db settings in conf/settings.py file. Activate you virtual environment and run:

```
pip install -r req.txt
python manage.py syncdb
python manage.py migrate-all
```