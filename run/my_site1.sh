#!/bin/bash

NAME=my_site
HOMEDIR=/home/alex/django_project
DJANGODIR=${HOMEDIR}/${NAME}
SOCKFILE=/tmp/${NAME}.sock
# Три рабочих процесса на 1 ядро процессора
NUM_WORKERS=3
DJANGO_WSGI_MODULE=${NAME}.wsgi
GUNICORN=/home/alex/django_project/env/bin/gunicorn

cd $DJANGODIR
source ${HOMEDIR}/venv/bin/activate

# Если по какой-то причине директории с SOCKFILE не существует -- создаем её
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Запускаем наш Django-проект
exec ${GUNICORN} ${DJANGO_WSGI_MODULE}:application \
  --workers $NUM_WORKERS \
  --bind unix:${SOCKFILE} \