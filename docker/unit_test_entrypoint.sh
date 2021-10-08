#!/bin/bash

python manage.py migrate --settings=core.settings.test --no-input
python manage.py test apps --settings=core.settings.test --no-input
