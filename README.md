# festival-tts-arabic-voices-docker
A Docker image for a relatively light-weight full Arabic speech synthesis system

# Running the server

```
$ docker kill festival
$ docker rm festival
$ docker build -t festival-arabic:latest .
$ docker run -p 8080:8080 --name festival festival-arabic:latest
```

This will take about 20 mins

# Accessing the server

* In a browser: http://localhost:8080/shakkala/synth/file/<text_to_synthesise>
* In a browser: http://localhost:8080/mishkal/synth/file/<text_to_synthesise>
* NOTE if you are running docker on Windows (or with a docker machine in general) get the ip of the machine and use it instead of localhost above

