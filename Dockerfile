FROM python:3.9.1

RUN apt -y update && apt -y dist-upgrade

RUN echo "hello"

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

WORKDIR /home/

RUN git clone https://github.com/abel9851/starscope.git

RUN echo "hello"

WORKDIR /home/starscope/

RUN echo "hello"

RUN pip install -r requirements.txt

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]