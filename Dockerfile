FROM python:3.9.1

RUN apt -y update && apt -y dist-upgrade

WORKDIR /home/

RUN echo "hi1"

RUN echo "fixing1"

RUN echo "fixing2"

RUN git clone https://github.com/abel9851/starscope.git

WORKDIR /home/starscope/

RUN pip install -r requirements.txt

RUN pip install mysqlclient

COPY ./.env /home/starscope

EXPOSE 8000

# po, mo 명령어 수정. 잘안되면 노마드코더 영상보고 하기
# 명령어도 노마드코더 보고 알아내기

CMD ["bash", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && django-admin compilemessages && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]