FROM python:alpine
EXPOSE 5000
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYCODE 1

WORKDIR app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python main.py