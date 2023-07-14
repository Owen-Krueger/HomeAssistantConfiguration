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
            self.listen_event(self.toggle_light, "zha_event", device_id = event["event_device_id"], command = event["command"], lights = event["lights"])

    """
    Turns light on if currently off and turns light off if currently on.
    """
    def toggle_light(self, event_name, data, kwargs):
        lights = kwargs["lights"]

        first_light = lights[0]
        # Prevents duplicate events from toggling the light more than once.
        if self.utils.recently_triggered(first_light):
            self.log("{} recently triggered. Not toggling.".format(lights))
            return

        # This is a work around where sometimes lights get out of sync.
        current_state = self.utils.is_entity_on(first_light)
        self.log("Toggle triggered for {}. Turning light {}.".format(lights, "off" if current_state else "on"))

        # Go through the lights and turn them all on/off.
        for light in lights:
            if current_state:
                self.turn_off(light)
            else:
                self.turn_on(light)