import hassapi as hass
from datetime import datetime, timedelta

"""
Utility functions to be used by other scripts.
"""
class Utils(hass.Hass):
    
    """
    Returns if the entity state is currently "on".
    """
    def is_entity_on(self, entity) -> bool:
        return self.get_state(entity) == "on"

    """
    Returns if the entity state is currently "home".
    """
    def is_entity_home(self, entity) -> bool:
        return self.get_state(entity) == "home"

    """
    Gets the time from the entity's state.
    """
    def get_time(self, entity):
        return self.parse_time(self.get_state(entity))

    """
    Returns if the entity has been triggered recently (within the
    number of seconds inputted or two seconds if not specified).
    """
    def recently_triggered(self, entity, seconds: int = 2) -> bool:
        last_changed = datetime.strptime(self.get_state(entity, attribute="all")["last_changed"], "%Y-%m-%dT%H:%M:%S.%f%z")

        return self.datetime(True) <= last_changed + timedelta(seconds=seconds)