FROM python:3.12-slim
WORKDIR /app
COPY . .
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/djangoapp/get_dealers')"
CMD ["python", "server.py"]

