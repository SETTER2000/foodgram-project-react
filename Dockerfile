# создать образ на основе базового слоя python (там будет ОС и интерпретатор Python)
FROM python:3.8.5

RUN mkdir /code

ENV DIRPATH=/code

#WORKDIR $DIRPATH

COPY requirements.txt $DIRPATH

RUN python3 -m pip install --upgrade pip && pip install -r $DIRPATH/requirements.txt --no-cache-dir

COPY . $DIRPATH

WORKDIR $DIRPATH

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

