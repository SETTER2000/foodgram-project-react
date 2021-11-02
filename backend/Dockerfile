FROM python:3.8.5

WORKDIR /code

COPY . .

WORKDIR ./backend

RUN pip3 install -r requirements.txt

RUN python manage.py collectstatic

CMD gunicorn grocery_assistant.wsgi:application --bind 0.0.0.0:8000
