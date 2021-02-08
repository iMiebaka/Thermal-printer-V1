#!/bin/sh

cd /home/imiebaka/Documents/Harvest/Hospital/python
source linux_evv/bin/activate
python manage.py makemigrations
python manage.py migrate

