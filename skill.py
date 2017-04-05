"""Alexa Skill to harness the power of the Giant Bomb API."""

import sys
import logging

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

from gb import api


app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
giant_bomb = api.GBApi()


@ask.launch
def launch():
    """Start the skill."""
    greeting_text = render_template('greeting')
    reprompt_text = render_template('reprompt')
    return question(greeting_text).reprompt(reprompt_text)


@ask.intent('GetAnswerIntent', mapping={'title': 'Title'}, default={'title': ''})
def answer(title):
    """The default intent to be triggered. Uses the title to search the GB API.

    :param title: the title to search in the wiki database
    :returns: a `flask-ask.statement` result with the given template text

    """
    if not title:
        nothing_text = render_template('nothing')
        return question(nothing_text)
    lookup = giant_bomb.whatis(title)
    print("Lookup: {}".format(lookup))
    if lookup.match:
        found_text = render_template('found', name=lookup.name, release=lookup.release_human, 
                                     deck=lookup.deck)
        return statement(found_text)
    notfound_text = render_template('notfound', name=title)
    more_text = render_template('more')
    return statement(notfound_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    """Give the user the help text."""
    help_text = render_template('reprompt')
    return question(help_text).reprompt(help_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    """Allow the user to stop interacting."""
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    """Allow the user to cancel the interaction."""
    return statement("Goodbye")


@ask.session_ended
def session_ended():
    """End the session gracefully."""
    return "", 200


def main():
    """Utility method to run the app if outside of lambda."""
    app.run()


if __name__ == '__main__':
    main()