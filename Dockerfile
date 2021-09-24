FROM python:3.9.1

RUN apt -y update && apt -y dist-upgrade

RUN echo "hello"

WORKDIR /home/

RUN git clone https://github.com/abel9851/starscope.git

WORKDIR /home/starscope/

RUN pip install -r requirements.txt

RUN pip install mysqlclient

COPY ./.env /home/starscope

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]