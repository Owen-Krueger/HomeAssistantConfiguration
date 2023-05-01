import hassapi as hass

"""
Automation to toggle lights on and off due to events received.
"""
class ToggleableLighting(hass.Hass):

    """
    Sets up the automations.
    """
    def initialize(self):
        self.utils = self.get_app("utils")

        for event in self.args["dictionary"]:
            self.listen_event(self.toggle_light, "zha_event", device_id = event["event_device_id"], command = event["command"], light = event["light"])

    """
    Turns light on if currently off and turns light off if currently on.
    """
    def toggle_light(self, event_name, data, kwargs):
        light = kwargs["light"]
        
        # Prevents duplicate events from toggling the light more than once.
        if self.utils.recently_triggered(light):
            self.log("{} recently triggered. Not toggling.".format(light))
            return

        current_state = self.utils.is_entity_on(light)
        self.log("Toggle triggered for {}. Turning light {}.".format(light, "off" if current_state else "on"))

        if (current_state):
            self.turn_off(light)
        else:
            self.turn_on(light)