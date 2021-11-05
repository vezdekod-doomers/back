FROM python:3.8-slim
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
USER root
RUN apt update -y && \
    apt install -y build-essential libblas-dev liblapack-dev gfortran libmariadb-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["flask", "run"]