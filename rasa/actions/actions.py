# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import logging

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        sender_id = tracker.current_state()['sender_id']
        user_message = tracker.latest_message.get('text')
        channel = tracker.get_latest_input_channel()
        logger.info(f'Received message: {dict(user_message=user_message, sender_id=sender_id, channel=channel)}"')

        dispatcher.utter_message(text=f"You said: {user_message}")

        return []
