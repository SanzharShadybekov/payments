FROM python:3

ENV PYTHONIOENCODING UTF-8
ENV PYTHONUNBUFFERED 1
ENV TZ=ASIA/Bishkek

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /usr/src/app

RUN chown -R nobody:nogroup /usr/src/app
RUN mkdir static && mkdir media && mkdir media/avatars

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
