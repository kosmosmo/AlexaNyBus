

"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
from scraper import Scraper
import heapq

# --------------- Helpers that build all of the responses ----------------------

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

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
global nex
nex = 0
def get_busno_response(busno):
    global buses
    global index
    global num
    global nex
    nex = False
    num = busno
    index = 0
    buses = Scraper().scraper(busno)
    if buses:
        speech_output = num + " is " + buses[index]
        index += 1
    else:
        speech_output = "no bus"
        nex = 0
    if index >= len(buses):
        nex = 0
    else:
        nex = 1
    session_attributes = {}
    card_title = "busno"
    reprompt_text = "Next bus?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_dest_response(dest):
    global heap
    global nex
    nex = 2
    heap = Scraper().destination(dest)
    if heap:
        cur = heapq.heappop(heap)
        if cur[0] <= 1:leave = "now!"
        else:leave = "in " + str(cur[0]) + " minutes."
        speech_output = cur[1] + ' is ' + cur[2] + " away. You better leave " + leave
    else:
        speech_output = "no bus available at the moment"
        nex = 0
    session_attributes = {}
    card_title = "dest"
    reprompt_text = "Next bus?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_next_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    global buses
    global index
    global nex
    global heap
    if nex == 0:
        speech_output = "no more buses"
    elif nex == 1:
        if index < len(buses):
            speech_output = "next " + num + " is " + buses[index]
            index += 1
        else:
            speech_output = "no bus"
            nex = 0
    elif nex == 2:
        if heap:
            cur = heapq.heappop(heap)
            if cur[0] <= 1:leave = "now!"
            else:leave = "in " + str(cur[0]) + " minutes."
            speech_output = cur[1] + ' is ' + cur[2] + " away. You better leave " + leave
        else:
            speech_output = "no more bus at the moment"
            nex = 0


    session_attributes = {}
    card_title = "Test"
    reprompt_text = "Hello?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "What's up"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Hello?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Ok.. Bye "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass



def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "twentysevenIntent":
        return get_busno_response("Q27")
    elif intent_name == "seventysixIntent":
        return get_busno_response("Q76")
    elif intent_name == "twentysixIntent":
        return get_busno_response("Q26")
    elif intent_name == "flushingIntent":
        return get_dest_response("flushing")
    elif intent_name == "cityIntent":
        return get_dest_response("city")
    elif intent_name == "cityIntent":
        return get_dest_response("test")
    elif intent_name == "nextIntent":
        return get_next_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
