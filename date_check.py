import boto3
import datetime
from __future__ import print_function

def lambda_handler(event, context):
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.0e284372-1b7e-406f-9e1f-502c259bf986"):
         raise ValueError("Invalid Application ID")

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])



def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    session_attributes = {}
    should_end_session = True
    card_title = intent['name']
    reprompt_text = "What is reprompt text for?"
    
    first_dose = datetime.date(2018,8,23)  #year, month, day
    days_left = datetime.date.today()-first_dose
    off_days = 4
    if (days_left.days % off_days) == 0 :
        speech_output = "Yes, Katara needs pee pee pills today"
    else :
        speech_output = "No, Katara does not need medicine today"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_response(session_attributes, speechlet_response):
        return {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': speechlet_response
        }

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
