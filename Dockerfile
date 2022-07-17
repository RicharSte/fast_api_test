FROM python:3.10.5-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r ./requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]