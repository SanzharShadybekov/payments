# Payments Online - Сайт для просмотра и проведения онлайн оплат за товары и услуги

## Технологический стек
- **Python**: версия 3.12.3.
- **Библиотеки**: Список библиотек находится в файле `requirements.txt`.
- **СУБД**: PostgreSQL.
- **Celery**: Планировщик асинхронных задач.
- **Redis**: Брокер сообщений для Celery.
## Установка и запуск проекта
### Клонирование проекта
```
git clone <url>
```
### Установка зависимостей
```
python -m venv venv
surce venv\bin\activate
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```
### Настройка локальной базы данных
```
create database payments;
```
### Конфигурация переменных окружения
```
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
REDIS_HOST=
REDIS_PORT=
EMAIL_USER=
EMAIL_PASSWORD=
```
### Применение миграций
```
python manage.py migrate
```

### Запуск Celery
Убедитесь, что Redis сервер установлен и работает:
```
redis-cli ping
```
Если сервер отвечает `PONG`, то Redis работает. Затем запустите Celery:
```
celery -A core worker --loglevel=info
celery -A core beat
```  
### Запуск приложения Django
```
python manage.py runserver
```

### Так же можно запустить через докер контейнеры 
* **Установка docker in ubuntu 20/22 instance** 
```
sudo apt update && sudo apt upgrade -y
sudo apt install ca-certificates curl gnupg lsb-release unzip
```
Добавление Docker’s GPG key
```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
Добавление official docker repo
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```
Установка docker
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Добавление user to docker group
```
sudo usermod -aG docker $USER
id $USER
newgrp docker
```
Установка docker-compose
```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Проверка docker and docker-compose
```
docker run hello-world
docker-compose --version
```
* ### Запуск docker containers
```
docker-compose up --build -d
```

## Ветвление в GIT
- **main**: Ветка для продакшн.

## Рекомендации для разработчиков
- Следовать стандарту PEP8.
- Использовать `flake8` в качестве линтера.
- Комментарии к коду должны быть на русском языке и написаны грамотно, с соблюдением правил пунктуации.
- Все TODO-комментарии должны быть четко формулированы.
- В файле Документация API Online Payments.docx описана документация для внедрения и интеграции сервсиса