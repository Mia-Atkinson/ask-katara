from __future__ import print_function
import boto3
import datetime
off_days = 4

def lambda_handler(event, context):
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.0e284372-1b7e-406f-9e1f-502c259bf986"):
         raise ValueError("Invalid Application ID")

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])



def on_intent(intent_request, session):

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    session_attributes = {}
    should_end_session = True
    card_title = intent['name']
    reprompt_text = "What is reprompt text for?"

    if intent_name == "WhosAGoodDog" :
        speech_output = good_dog_response()
    else :
        speech_output = medicine_response()

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def good_dog_response():
    return "Yes, they're good dogs"

def medicine_response():
    global off_days
    first_dose = datetime.date(2018,8,23)  #year, month, day
    days_left = datetime.date.today()-first_dose
    if (days_left.days % off_days) == 0 :
        return "Yes, Katara needs pee pee pills today"
    else :
        return "No, Katara does not need medicine today"

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
