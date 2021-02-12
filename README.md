# festival-tts-arabic-voices-docker
A Docker image for a relatively light-weight full Arabic speech synthesis system

# Running the server

1. Launch the server
```
$ git clone https://github.com/nawarhalabi/festival-tts-arabic-voices-docker
$ cd festival-tts-arabic-voices-docker
$ docker kill festival
$ docker rm festival
$ docker build -t festival-arabic:latest .
$ docker run -p 8080:8080 -v <wav files dir>:/tts --name festival festival-arabic:latest
```

This will take about 20 mins to finish. Bare in mind the ```<wav files dir>``` will contain the generated the wav files after sending the http request based on certain config below

2. Configure Apache or any webserver to serve the static file directory ```<wav files dir>``` through ```http://<hostname or ip>/tts/```
3. Use the following JS and HTML as a template for creating a web interface for using the voice:

```html
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
</head>
```

```html
<textarea id="input-text" dir="rtl" name="arabic-text" rows="5" placeholder="Please enter Arabic text"></textarea>
<input id="tts-btn-mishkal" type="button" name="synthesise-mishkal" value="Synthesise (Mishkal as diacritiser)">
<input id="tts-btn-shakkala" type="button" name="synthesise-shakkala" value="Synthesise (Shakkala as diacritiser)">
<audio controls="">
       <source id="source" src="" type="audio/wav">
       Browser does not support this
</audio>
<script>
tts_server = 'http://<hostname or ip>/tts/';

$('#tts-btn-mishkal').on('click', function(e) {
        $.getJSON({
                url: 'http://<hostname or ip>:8080/mishkal/synth/url/' + $('#input-text').val(),
                data: '',
                success: function( data ) {
                        $('audio #source').attr('src', tts_server + data['url']);
                        $('audio').get(0).load();
                        $('audio').get(0).play();
                }
        });
});

$('#tts-btn-shakkala').on('click', function(e) {
        $.getJSON({
                url: 'http://<hostname or ip>:8080/shakkala/synth/url/' + $('#input-text').val(),
                data: '',
                success: function( data ) {
                        $('audio #source').attr('src', tts_server + data['url']);
                        $('audio').get(0).load();
                        $('audio').get(0).play();
                }
        });
});
</script>
```

# Accessing the server

* For direct wav response:
  * In a browser: http://localhost:8080/shakkala/synth/file/<text_to_synthesise>
  * In a browser: http://localhost:8080/mishkal/synth/file/<text_to_synthesise>
* For file generation (This will respond with a json containing the name of the file to load from the server in a separate http request):
  * In a browser: http://localhost:8080/shakkala/synth/url/<text_to_synthesise>
  * In a browser: http://localhost:8080/mishkal/synth/url/<text_to_synthesise>
* NOTE if you are running docker on Windows (or with a docker machine in general) get the ip or hostname of the machine and use it instead of localhost above

