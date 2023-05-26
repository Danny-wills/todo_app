FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "gunicorn", "app:app", "--bind" , "0.0.0.0:8000", "--workers", "4"]