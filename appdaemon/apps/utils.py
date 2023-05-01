import hassapi as hass
import datetime

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