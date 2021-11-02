FROM python:3.8.5
<<<<<<< HEAD
WORKDIR /code
COPY .  .
COPY requirements/ requirements/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements/develop.txt
CMD gunicorn configuration.wsgi:application --bind 0.0.0.0:8000
=======

WORKDIR /code

COPY . .

WORKDIR ./backend

RUN pip3 install -r requirements.txt

RUN python manage.py collectstatic

CMD gunicorn grocery_assistant.wsgi:application --bind 0.0.0.0:8000
>>>>>>> dev
