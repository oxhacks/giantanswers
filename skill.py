import sys

from flask import flask
from flask_ask import Ask, statement, question, session

from gb import api


app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launch():
    greeting_text = render_template('greeting')
    reprompt_text = render_template('reprompt')
    speech = question(greeting_text).reprompt(reprompt_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('reprompt')
    return question(help_text).reprompt(help_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    api = api.GBApi()
    print(api.whatis(sys.argv[1]))