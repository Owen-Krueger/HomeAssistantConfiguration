import hassapi as hass
import datetime
import json

"""
Utility functions to be used by other scripts.
"""
class Utils(hass.Hass):
    
    """
    Returns if the entity state is currently "on".
    """
    def is_entity_on(self, entity):
        return self.get_state(entity) == "on"

    """
    Returns if the entity state is currently "home".
    """
    def is_entity_home(self, entity):
        return self.get_state(entity) == "home"

    """
    Gets the time from the entity's state.
    """
    def get_time(self, entity):
        return self.parse_time(self.get_state(entity))

    """
    Returns "on" if state "off" and "off" if state "on"
    """
    def get_opposite_state(self, state: str) -> str:
        return "on" if state == "off" else "off"

    """
    Gets JSON from the file at the input file path.
    """
    def get_json_from_file(self, file_name: str):
        file = open("/config/appdaemon/apps/data/{}.json".format(file_name))
        data = json.load(file)
        file.close()
        return data

    """
    Gets the data from the data file and sends it to the user.
    """
    def notify_user(self, user: str, file_name: str):
        self.log("Sending message to {}".format(user))
        data = self.get_json_from_file(file_name)
        message = data['message']
        del data['message']
        self.log(json.dumps(data))
        self.notify(message, name = user, data = json.dumps(data))
        self.log("Message sent!")