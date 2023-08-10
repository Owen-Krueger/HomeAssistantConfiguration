import hassapi as hass

"""
Away lighting automations.
"""
class AwayLighting(hass.Hass):
    
    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.should_turn_off_lights = self.args["should_turn_off_lights"]
        self.all_off = self.args["all_off"]
        self.all_off_dynamic = self.args["all_off_dynamic"]
        self.allison = self.args["allison"]
        self.downstairs_lights = self.args["downstairs_lights"]
        self.downstairs_tv_on = self.args["downstairs_tv_on"]
        self.mode_guest = self.args["mode_guest"]
        self.office_lights = self.args["office_lights"]
        self.owen = self.args["owen"]
        self.owen_computer_active = self.args["owen_computer_active"]
        self.upstairs_tv_on = self.args["upstairs_tv_on"]
        self.uptsairs_living_area_off = self.args["uptsairs_living_area_off"]

        if self.utils.is_entity_on(self.should_turn_off_lights): # Only run automations if boolean is on
            self.set_up_triggers()

        self.listen_state(self.on_should_turn_off_lights_change, self.should_turn_off_lights, duration = 60) # Only update the automation triggers when boolean has been set for 60 seconds.

    """
    Sets up triggers for presence and time triggers.
    """
    def set_up_triggers(self):
        self.allison_presence_handler = self.listen_state(self.away_lighting, self.allison, new = "not_home", duration = 300) # When away for 5 minutes
        self.owen_presence_handler = self.listen_state(self.away_lighting, self.owen, new = "not_home", duration = 300) # When away for 5 minutes

    """
    On automation boolean change, cancel triggers if they're active and
    re-set them up if they're currently disabled.
    """
    def on_should_turn_off_lights_change(self, entity, attribute, old, new, kwargs):
        self.log("Automation turned {}".format(new))

        if (old == "on"): # Cancel old triggers if they were active.
            self.cancel_listen_state(self.allison_presence_handler)
            self.cancel_listen_state(self.owen_presence_handler)

        if (new == "on"):
            self.set_up_triggers()

    """
    Checks who is home. If everyone is gone, all lights are turned off.
    If only Allison is gone and Owen is at work, turn on office lighting.
    """
    def away_lighting(self, entity, attribute, old, new, kwargs):
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
            self.away_lighting_dynamic()

    """
    Turns off all lights that don't change based on logic, and then
    turns off any lights that are on and don't have activity in that room.
    """
    def away_lighting_dynamic(self):
        self.turn_on(self.all_off_dynamic)

        # Upstairs Living Area (Kitchen and living room)
        if not self.utils.is_entity_on(self.upstairs_tv_on):
            self.turn_on(self.uptsairs_living_area_off)
        
        # Downstairs Lights
        if (self.utils.is_entity_on(self.downstairs_lights) and
            not self.utils.is_entity_on(self.downstairs_tv_on)):
            self.turn_off(self.downstairs_lights)

        # Office Lights
        if (self.utils.is_entity_on(self.office_lights) and
            not self.utils.is_entity_on(self.owen_computer_active)):
            self.turn_off(self.office_lights)