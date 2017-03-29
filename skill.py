import sys

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

from gb import api


app = Flask(__name__)
ask = Ask(app, '/')
giant_bomb = api.GBApi()


@ask.launch
def launch():
    greeting_text = render_template('greeting')
    reprompt_text = render_template('reprompt')
    speech = question(greeting_text).reprompt(reprompt_text)


@ask.intent('GetAnswerIntent', mapping={'title': 'Title'})
def answer(title):
    lookup = giant_bomb.whatis(title)
    print("Lookup: {}".format(lookup))
    if lookup.match:
        found_text = render_template('found', name=lookup.name, release=lookup.release_human, 
                                     deck=lookup.deck)
        return statement(found_text)
    notfound_text = render_template('notfound', name=title)
    return statement(notfound_text)


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

def main():
    app.run()


if __name__ == '__main__':
    main()