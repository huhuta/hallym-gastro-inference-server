FROM tiangolo/uwsgi-nginx-flask:python3.6
WORKDIR /app
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /app

