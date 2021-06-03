# Object Definitions
object_list = ["coloredcow"]

object_definition = {"coloredcow":"We build remarkable web and mobile applications."}

# Event handler functions
def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()
        
# Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Hi! I'm ColoredCow's assistant. How can I help you?"
    reprompt_MSG = "Would you like to know about ColoredCow?"
    card_TEXT = "How can I help you?"
    card_TITLE = "Need help"
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")
    
# Handle Intent
def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "aboutColoredCow":
        return about_coloredcow(event)        
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)
        
# Intent handler functions
def about_coloredcow(event):
    name=event['request']['intent']['slots']['object']['value']
    object_list_lower=[w.lower() for w in object_list]
    if name.lower() in object_list_lower:
        reprompt_MSG = "Do you want to hear more about ColoredCow?"
        card_TEXT = "About " + name.lower()
        card_TITLE = "About " + name.lower()
        return output_json_builder_with_reprompt_and_card(object_definition[name.lower()], card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "I'm not sure about that."
        reprompt_MSG = "Do you want to hear more about ColoredCow?"
        card_TEXT = "I'm not sure about that."
        card_TITLE = "I'm not sure about that."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
        
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "I can tell you about ColoredCow"
    reprompt_MSG = "Do you want to hear about ColoredCow?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear about ColoredCow?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    
# Response helper functions
    
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict
    
    
