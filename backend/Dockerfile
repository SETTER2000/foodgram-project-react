FROM python:3.8.5

WORKDIR /code

COPY . .

WORKDIR ./backend

RUN python -m pip install --upgrade pip && \
pip3 install -r requirements.txt --no-cache-dir


RUN python manage.py collectstatic

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

