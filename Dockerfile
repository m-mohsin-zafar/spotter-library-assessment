FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile Pipfile.lock /usr/src/app/

RUN pipenv install --deploy --ignore-pipfile

COPY . /usr/src/app/

EXPOSE 8000

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]