docker kill festival
docker rm festival
docker build -t festival-arabic:latest .
docker run -d -v /var/www/production/ar/tts:/tts -p 8080:8080 --name festival festival-arabic:latest
