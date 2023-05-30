import hassapi as hass

"""
For notifying when entities have become unavailable.
"""
class UnavailableEntities(hass.Hass):
    
    """
    Sets up the automation.
    """
    def initialize(self):
        for entity in self.args["list"]:
            self.listen_state(self.notify_owen, entity, new = "unavailable")

    """
    Notify Owen that the entity has become unavailable.
    """
    def notify_owen(self, entity, attribute, old, new, kwargs):
        message = "{} is unavailable.".format(entity)
        self.log("{} Notifying.".format(message))
        self.notify(message, name="owen")