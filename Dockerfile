FROM python:3.7

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

#EXPOSE 8000

ENV TZ Europe/Moscow

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]