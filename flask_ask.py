import logging
import os
from scraper import Scraper
from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

i = 0
a= None
@ask.launch
def launch():
    speech_text = "whats up dawg..."
    return question(speech_text)


@ask.intent('twentysevenIntent')
def bus():
    global i
    global a
    i = 0
    inf = Scraper().scraper("https://bustime.mta.info/m/index?q=501680")
    if inf:
        print (inf)
        a = inf["Q27"]
        speech_text = a[0]
        i += 1
    else:
        return statement("No busses")
    if i >= len(a):
        return statement(speech_text)
    else:
        return question(speech_text + "...next?" )

@ask.intent('seventysixIntent')
def bus():
    global i
    global a
    i = 0
    inf = Scraper().scraper("https://bustime.mta.info/m/index?q=502760")
    if inf:
        print (inf)
        a = inf["Q76"]
        speech_text = a[0]
        i += 1
    else:
        return statement("No busses")
    if i >= len(a):
        return statement(speech_text)
    else:
        return question(speech_text + "...next?" )

@ask.intent('yesIntent')
def nextbus():
    global i
    global a

    if i == len(a):
        return statement("No more buses")
    else:
        speech_text = a[i]
        i += 1
    return question(speech_text + "...next bus?")

@ask.intent('noIntent')
def nextbus():
    return statement("Later dawg.")


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)