import hassapi as hass

"""
Turning lights off automations.
"""
class OffLighting(hass.Hass):
    
    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.all_off = self.args["all_off"]
        self.all_off_dynamic = self.args["all_off_dynamic"]
        self.allison = self.args["allison"]
        self.downstairs_lights = self.args["downstairs_lights"]
        self.downstairs_tv_on = self.args["downstairs_tv_on"]
        self.mode_guest = self.args["mode_guest"]
        self.office_lights = self.args["office_lights"]
        self.owen = self.args["owen"]
        self.owen_computer_active = self.args["owen_computer_active"]
        self.owen_phone_charger_type = self.args["owen_phone_charger_type"]
        self.night_lighting = self.args["night_lighting"]
        self.upstairs_tv_on = self.args["upstairs_tv_on"]
        self.upstairs_living_area_off = self.args["upstairs_living_area_off"]
        self.vacation_mode = self.args["vacation_mode"]

        self.listen_state(self.turn_off_lights, self.allison, new = "not_home", duration = 300) # When away for 5 minutes.
        self.listen_state(self.turn_off_lights, self.owen, new = "not_home", duration = 300) # When away for 5 minutes.
        self.listen_state(self.turn_off_lights_at_night, self.owen_phone_charger_type, new = "wireless", duration = 10) # When phone charging for 10 seconds.
        self.listen_event(self.active_night_lighting, "CUSTOM_EVENT_NIGHT_LIGHTING") # When a night lighting event is triggered.

    """
    Checks who is home. If everyone is gone, all lights are turned off.
    If only Allison is gone and Owen is at work, turn on office lighting.
    """
    def turn_off_lights(self, entity, attribute, old, new, kwargs):
        self.log("Executing automation.")
        if self.utils.is_entity_on(self.mode_guest):
            return

        owen_home = self.utils.is_entity_home(self.owen)
        allison_home = self.utils.is_entity_home(self.allison)

        if not owen_home and not allison_home:
            self.log("Everyone away. Turning off all lights.")
            self.turn_on(self.all_off)
        else:
            self.log("Turning off lights depending on state.")
            self.turn_on(self.all_off_dynamic)
            self.turn_off_lights_based_on_state()

    """
    Turns on night lighting scene.
    """
    def active_night_lighting(self, event_name, data, kwargs):
        self.log("Turning on night lighting.")
        self.turn_on(self.night_lighting)
        self.turn_off_lights_based_on_state()

    """
    Turns off any lights that are on and don't have activity in that room.
    """
    def turn_off_lights_based_on_state(self):
        # Upstairs Living Area (Kitchen and living room)
        if not self.utils.is_entity_on(self.upstairs_tv_on):
            self.turn_on(self.upstairs_living_area_off)
        
        # Downstairs Lights
        if (self.utils.is_entity_on(self.downstairs_lights) and
            not self.utils.is_entity_on(self.downstairs_tv_on)):
            self.turn_off(self.downstairs_lights)

        # Office Lights
        if (self.utils.is_entity_on(self.office_lights) and
            not self.utils.is_entity_on(self.owen_computer_active)):
            self.turn_off(self.office_lights)

    """
    At night, turn off all lights in the house once people are sleeping.
    """
    def turn_off_lights_at_night(self, entity, attribute, old, new, kwargs):
        if (not self.utils.is_entity_on(self.vacation_mode) and
            self.utils.is_entity_home(self.owen) and
            self.now_is_between("20:30:00", "03:00:00")):
            self.log("Turning off all lights due to phone charging at night.")
            self.turn_on(self.all_off)