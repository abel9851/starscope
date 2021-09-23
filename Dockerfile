FROM python:3.9.1

RUN apt -y update && apt -y dist-upgrade

WORKDIR /home/starscope/

COPY ./requirements.txt /srv

RUN pip install -r /srv/requirements.txt

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]