import hassapi as hass

"""
Bedroom lighting automations.
"""
class BedroomLighting(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.bedroom_button_device_id = self.args["bedroom_button_device_id"]
        self.bedroom_lamps = self.args["bedroom_lamps"]
        self.bedroom_lights = self.args["bedroom_lights"]

        self.listen_event(self.on_bedside_button_click, "zha_event", device_id = self.bedroom_button_device_id, command = "single")
        self.listen_state(self.on_bedroom_lights_turned_off, self.bedroom_lights, new = "off")

    """
    On bedroom bedside button clicked, toggle the bedroom lamps.
    If late and bedroom lights on, also turn them off.
    """
    def on_bedside_button_click(self, event_name, data, kwargs):
        self.toggle(self.bedroom_lamps)

        if self.is_late() and self.utils.is_entity_on(self.bedroom_lights):
            self.turn_off(bedroom_lights)

    """
    If late, turn on bedroom lamps.
    """
    def on_bedroom_lights_turned_off(self, entity, attribute, old, new, kwargs):
        if not self.is_late():
            return

        self.turn_on(self.bedroom_lamps)

    """
    Returns if it's late at night.
    """
    def is_late(self) -> bool:
        return self.now_is_between("21:00:00", "23:59:59")