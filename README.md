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
## Ветвление в GIT
- **main**: Ветка для продакшн.
- **dev**: Ветка для тестирования.
## Рекомендации для разработчиков
- Следовать стандарту PEP8.
- Использовать `flake8` в качестве линтера.
- Комментарии к коду должны быть на русском языке и написаны грамотно, с соблюдением правил пунктуации.
- Все TODO-комментарии должны быть четко формулированы.