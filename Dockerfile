FROM debian

RUN apt-get update
RUN apt-get install -y festival
RUN apt-get install -y htsengine
RUN apt-get install -y git
RUN apt-get install -y build-essential
RUN apt-get install -y sudo
RUN apt-get install -y zip unzip
RUN apt-get install -y python2
RUN apt-get install -y python3
RUN apt-get install -y python-pip
RUN apt-get install -y python3-pip
RUN pip3 install flask
RUN pip3 install gunicorn

RUN cd ~;git clone https://github.com/linuxscout/festival-tts-arabic-voices.git
RUN cd ~/festival-tts-arabic-voices; make install

RUN cd ~;git clone https://github.com/linuxscout/mishkal.git
RUN pip install -r ~/mishkal/requirements.txt

RUN cd ~;git clone https://github.com/Barqawiz/Shakkala
RUN pip install -r ~/Shakkala/requirements/requirements.txt

RUN pip3 install nltk==3.5
RUN pip3 install tensorflow==1.14.0
RUN pip3 install keras==2.2.0
RUN cp /root/Shakkala/Shakkala.py /root/Shakkala.py
RUN cp /root/Shakkala/helper.py /root/helper.py
RUN cp /root/Shakkala/demo.py /root/demo.py
RUN cp -r /root/Shakkala/dictionary /root/Shakkala/model/dictionary

COPY filter.py /root/filter.py
COPY server.py /root/server.py

#CMD cd /root ; gunicorn -w 10 -b 0.0.0.0:8080 server:app
CMD cd /root ; python3 server.py
