import hassapi as hass

"""
For automations based on the computer being active.
"""
class WorkLighting(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.dining_room_lights = self.args["dining_room_lights"]
        self.is_work_day = self.args["is_work_day"]
        self.office_lights = self.args["office_lights"]
        self.owen = self.args["owen"]
        self.owen_computer_active = self.args["owen_computer_active"]

        self.listen_state(self.on_computer_active, self.owen_computer_active, new = "on", duration = 60) # When computer active for 60 seconds
        self.listen_state(self.on_computer_inactive, self.owen_computer_active, new = "off", duration = 120) # When computer inactive for 120 seconds

    """
    Automations when computer is active.
    Turns on office lights if they're currently off.
    """
    def on_computer_active(self, entity, attribute, old, new, kwargs):
        self.log("Executing automations due to computer being active.")

        if not self.utils.is_entity_on(self.office_lights):
            self.turn_on(self.office_lights)

    """
    Automations when computer is inactive.
    Turns off office lights if they're currently on. Turns on dining room lights
    if they're currently off.
    """
    def on_computer_inactive(self, entity, attribute, old, new, kwargs):
        self.log("Executing automatinos due to computer being inactive.")

        if self.utils.is_entity_on(self.office_lights):
            self.log("Turning off office lights.")
            self.turn_off(self.office_lights)

        # If Owen is home, it's a work day, and it's around lunch time.
        if (not self.utils.is_entity_on(self.dining_room_lights) and
            self.utils.is_entity_home(self.owen) and
            self.utils.is_entity_on(self.is_work_day) and
            self.now_is_between("11:00:00", "13:30:00")):
            self.log("Turning on dining room lights.")
            self.turn_on(self.dining_room_lights)