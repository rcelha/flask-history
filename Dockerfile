FROM python:3-onbuild

ADD requirements.txt /requirements.txt
ADD flask_history /code/flask_history

WORKDIR /code/flask_history

EXPOSE 5000

CMD ["python", "main.py"]
