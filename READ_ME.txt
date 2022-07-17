docker pull mongo:latest  #скачиваем базу монги
docker run -d -p 27017:27017 --name mongo mongo #запускаем монгу чтобы залить записи
python3 app/upload_data.py #загружаем записи в монгу (Тезнически можно и в докере это делать)

docker build -t fast_api . #делаем докер image
docker run -d --name fast_api -p 80:80 fast_api # запускаем его на 80м порту