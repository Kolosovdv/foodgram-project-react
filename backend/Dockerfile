FROM python:3.7-slim
# Сделать директорию /app рабочей директорией. 
WORKDIR /app
# Создать директорию вашего приложения.

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY backend/requirements.txt .

RUN python3 -m pip install --upgrade pip


# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r requirements.txt --no-cache-dir

# Скопировать содержимое директории /api_yamdb c локального компьютера
# в директорию /app.
COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ] 