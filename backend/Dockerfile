


FROM python:3.7-slim

COPY ./ /app

WORKDIR /app

COPY requirements.txt pwd

RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt --no-cache-dir

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 
# FROM python:3.7-slim
# WORKDIR /app
# # Запустить команду создания директории внутри контейнера

# COPY backend/ .
# # Скопировать с локального компьютера файл зависимостей
# # в директорию /app.
# #COPY backend/requirements.txt /app

# # Выполнить установку зависимостей внутри контейнера.
# RUN pip3 install -r /requirements.txt --no-cache-dir

# CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 