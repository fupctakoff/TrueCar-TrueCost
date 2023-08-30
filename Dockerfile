FROM python:3.10-slim

WORKDIR /django-app

COPY requirements.txt .
RUN pip install -r requirements.txt

#copy project
COPY . .

CMD ["python", "tctc/manage.py", "runserver", "0.0.0.0:80"]