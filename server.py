from flask import Flask, send_file, request
import codecs
import subprocess
import time
import random
import Shakkala as sh
from keras.models import load_model
from shakkelha.shakkelha import *
from shakkelha.optimizer import *

shakkelha_mod = load_model('models/shakkelha.h5')
shakkelha_mod._make_predict_function()
app = Flask(__name__)

sh = sh.Shakkala("/root/Shakkala/", version=3)
model, graph = sh.get_model()

@app.route('/mishkal/synth/<text>')
def mishkal(text):
    try:
        rand = str(random.randint(0,9999999999))
        exit_codes = []
        
        p1 = subprocess.Popen(["python", "/root/mishkal/bin/mishkal-console.py", text], stdout=open("/tts/stage1_" + rand, 'w'), stderr=open("/tts/p1err", 'w'))
        exit_codes.append(p1.wait())
        p2 = subprocess.Popen(["python3", "/root/filter.py", "/tts/stage1_" + rand, "/tts/stage2_" + rand], stderr=open("/tts/p2err", 'w'))
        exit_codes.append(p2.wait())
        p3 = subprocess.Popen(["text2wave", "-eval", "(voice_ara_norm_ziad_hts)",  "-o", "/tts/out_" + rand + ".wav"], stdin=open("/tts/stage2_" + rand, 'r'), stderr=open("/tts/p3err", 'w'))
        exit_codes.append(p3.wait())
        
        return send_file('/tts/out_' + rand + '.wav', attachment_filename='out.wav')
    except Exception as e:
        return str(e) + str(exit_codes)
        
@app.route('/shakkala/synth/<text>')
def shakkala(text):
    try:
        rand = str(random.randint(0,9999999999))
        exit_codes = []
        
        input_int = sh.prepare_input(text)
        with graph.as_default():
          logits = model.predict(input_int)[0]
        predicted_harakat = sh.logits_to_text(logits)
        final_output = sh.get_final_text(text, predicted_harakat)
        
        with open('/tts/stage1_' + rand, 'w') as f:
            f.write(final_output)
            
        p1 = subprocess.Popen(["python3", "/root/filter.py", "/tts/stage1_" + rand, "/tts/stage2_" + rand], stderr=open("/tts/p2err", 'w'))
        exit_codes.append(p1.wait())
        p2 = subprocess.Popen(["text2wave", "-eval", "(voice_ara_norm_ziad_hts)",  "-o", "/tts/out_" + rand + ".wav"],
		                      stdin=open("/tts/stage2_" + rand, 'r'), stderr=open("/tts/p3err", 'w'))
        exit_codes.append(p2.wait())
        
        return send_file('/tts/out_' + rand + '.wav', attachment_filename='out.wav')
    except Exception as e:
        return str(e) + str(exit_codes)
        
@app.route('/shakkelha/synth/<text>')
def shakkelha(text):
    try:
        rand = str(random.randint(0,9999999999))
        exit_codes = []
        
        final_output = predict(text, shakkelha_mod)
        
        with open('/tts/stage1_' + rand, 'w') as f:
            f.write(final_output)
            
        p1 = subprocess.Popen(["python3", "/root/filter.py", "/tts/stage1_" + rand, "/tts/stage2_" + rand], stderr=open("/tts/p2err", 'w'))
        exit_codes.append(p1.wait())
        p2 = subprocess.Popen(["text2wave", "-eval", "(voice_ara_norm_ziad_hts)",  "-o", "/tts/out_" + rand + ".wav"],
		                      stdin=open("/tts/stage2_" + rand, 'r'), stderr=open("/tts/p3err", 'w'))
        exit_codes.append(p2.wait())
        
        return send_file('/tts/out_' + rand + '.wav', attachment_filename='out.wav')
    except Exception as e:
        return str(e) + str(exit_codes)
        

        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
