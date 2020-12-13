import random
import logging
import json
import prompts
import pymongo
import random
import requests 
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream)
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class LaunchHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In Launch Request Handler")
        access_token = handler_input.request_envelope.context.system.user.access_token
        if access_token is None:
            speech = prompts.AUTH_MESSAGE
            handler_input.response_builder.speak(speech)
            return handler_input.response_builder.response
        # get localization data
        else:
            logger.info(access_token)
            URL = "https://www.googleapis.com/oauth2/v1/userinfo"
            PARAMS = {'access_token':access_token} 
            r=requests.get(url = URL, params = PARAMS)
            data = r.json() 
            username= data["given_name"]
            data = handler_input.attributes_manager.request_attributes["_"]
            speech = "hello "+ username+" ,"+prompts.WELCOME_MESSAGE
            reprompt=prompts.WELCOME_REPROMPT
            handler_input.response_builder.speak(speech).ask(reprompt)
            return handler_input.response_builder.response

    
class PlayFileHandler(AbstractRequestHandler):
    """Handler for Playing audio on different events.
    Handles PlayAudio Intent, Resume Intent.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("IntentRequest")(handler_input)
                and is_intent_name("GetAudioIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In StartPlaybackHandler")
        speechText = handler_input.request_envelope.request.intent.slots
        filename=speechText['audioQuery'].value
        data = handler_input.attributes_manager.request_attributes["_"]
        logger
        if filename in data:
            return Controller.play(handler_input,filename)
        else:
            handler_input.response_builder.speak("FILE DOES NOT EXIST, PLEASE PROVIDE CORRECT INPUT").ask("TRY WITH A VALID FILENAME")
            return handler_input.response_builder.response  
        
class PlaySummryFileHandler(AbstractRequestHandler):
    """Handler for Playing audio on different events.
    Handles PlayAudio Intent, Resume Intent.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("IntentRequest")(handler_input)
                and is_intent_name("GetSmmryAudioIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In StartPlaybackHandler")
        speechText = handler_input.request_envelope.request.intent.slots
        filename=speechText['audiofile'].value
        data = handler_input.attributes_manager.request_attributes["_"]
        if filename in data:
            filename=filename+'_summarized'
            return Controller.play(handler_input,filename)
        else:
            handler_input.response_builder.speak("FILE DOES NOT EXIST, PLEASE PROVIDE CORRECT INPUT").ask("TRY WITH A VALID FILENAME")
            return handler_input.response_builder.response          
        

class ListFileHandler(AbstractRequestHandler):
    """Handler for Playing audio on different events.
    Handles PlayAudio Intent, Resume Intent.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("IntentRequest")(handler_input)
                and is_intent_name("ListFileIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In StartPlaybackHandler")
        data = handler_input.attributes_manager.request_attributes["_"]
        if(len(data)==0):
            handler_input.response_builder.speak("NO FILES EXIST IN DATABASE").ask("YOU VISIT WEBSITE TO UPLOAD FILE")
            return handler_input.response_builder.response
            
        index=random.randint(0,len(data));
        message="here are the files uploaded"
        for i in range(0,len(data)):
            message=message+", "+data[i]
        logger.info(message)
        handler_input.response_builder.speak(message).ask("You can say play filename, to start playing file")
        return handler_input.response_builder.response
    
    
class PlayRadioHandler(AbstractRequestHandler):
    """Handler for Playing audio on different events.
    Handles PlayAudio Intent, Resume Intent.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("IntentRequest")(handler_input)
                and (is_intent_name("GetRadioIntent")(handler_input) or is_intent_name("AMAZ0N.NextIntent")(handler_input)) )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In StartPlaybackHandler")
        data = handler_input.attributes_manager.request_attributes["_"]
        if(len(data)==0):
            handler_input.response_builder.speak("NO FILES EXIST IN DATABASE").ask("YOU VISIT WEBSITE TO UPLOAD FILE")
            return handler_input.response_builder.response
            
        index=random.randint(0,len(data));
        filename=data[index]+"_summarized"
        logger.info(filename)
        return Controller.play(handler_input,filename)
    
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        # get localization data

        speech = prompts.HELP_MESSAGE
        reprompt = prompts.HELP_REPROMPT
        handler_input.response_builder.speak(speech).ask(
            reprompt)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")


        return Controller.stop(handler_input)




class Controller:
    """Audioplayer and Playback Controller."""
    @staticmethod
    def play(handler_input, filename):
        # type: (HandlerInput) -> Response
        
        response_builder = handler_input.response_builder
        play_behavior = PlayBehavior.REPLACE_ALL
        audioUrl="https://inanutshell-mediafiles.s3.amazonaws.com/"+filename+".mp3"
        speech="playing "+filename+" audio file"
        response_builder.speak(speech).add_directive(
            PlayDirective(
                play_behavior=play_behavior,
                audio_item=AudioItem(
                    stream=Stream(
                        token=0,
                        url=audioUrl,
                        offset_in_milliseconds=0,
                        expected_previous_token=None),
                    metadata=None))
        ).set_should_end_session(True)
        
        return response_builder.response

    @staticmethod
    def stop(handler_input):
        # type: (HandlerInput) -> Response
        handler_input.response_builder.add_directive(StopDirective())
        return handler_input.response_builder.response
    
    
# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak("Sorry, I am unable to understand, for help ask hey cloud and say you need help").ask(
            "help")

        return handler_input.response_builder.response


    
class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """
    def findAll(self,SampleTable,email): 
        queryObject = {"user_email": email} 
        query = SampleTable.find(queryObject,{ "_id":0,"filename": 1 }) 
        output = []
        i = 0
        for x in query: 
            output.append(x) 
        output_doc =[]
        for x in output:
            output_doc.append(x['filename'])
        return (output_doc) 

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        #persistence_attr = handler_input.attributes_manager.persistent_attributes
        logger.info("Locale is {}".format(locale[:2]))
        access_token = handler_input.request_envelope.context.system.user.access_token
        
        if access_token is None:
            email="akhil"
        else:
            URL = "https://www.googleapis.com/oauth2/v1/userinfo"
            PARAMS = {'access_token':access_token} 
            r=requests.get(url = URL, params = PARAMS)
            data = r.json()
            logger.info(data)
            email= data["email"]
            
            
        logger.info(email)
        connection_url = 'mongodb+srv://username:password@inanutshellcluster.e1yvh.mongodb.net/InANutShell_DB?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connection_url) 
        Database = client.get_database('InANutShell_DB')
        FullTable = Database.inanutshell_app_files 
        filenames = self.findAll(FullTable,email)
        logger.info(filenames)
        handler_input.attributes_manager.request_attributes["_"] = filenames
        
    
    
    
# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(LaunchHandler())
sb.add_request_handler(PlayFileHandler())
sb.add_request_handler(PlayRadioHandler())
sb.add_request_handler(PlaySummryFileHandler())
sb.add_request_handler(ListFileHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())


# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
