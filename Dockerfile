# создать образ на основе базового слоя python (там будет ОС и интерпретатор Python)
FROM python:3.8.5
LABEL author='lphp@mail.ru' version=1 broken_keyboards=50

ENV DIRPATH=/code

WORKDIR $DIRPATH

COPY requirements.txt $DIRPATH

RUN pip install -r $DIRPATH/requirements.txt

COPY . $DIRPATH

WORKDIR $DIRPATH

#CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

