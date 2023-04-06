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
        self.allison = self.args["allison"]
        self.owen = self.args["owen"]
        self.all_off = self.args["all_off"]
        self.day_office = self.args["day_office"]
        self.is_work_day = self.args["is_work_day"]

        if self.utils.is_entity_on(self.should_turn_off_lights): # Only run automations if boolean is on
            self.set_up_triggers()

        self.listen_state(self.on_should_turn_off_lights_change, self.should_turn_off_lights, duration = 60) # Only update the automation triggers when boolean has been set for 60 seconds.

    """
    Sets up triggers for presence and time triggers.
    """
    def set_up_triggers(self):
        self.allison_presence_handler = self.listen_state(self.away_lighting, self.allison, duration = 300) # When away for 5 minutes
        self.owen_presence_handler = self.listen_state(self.away_lighting, self.owen, duration = 300) # When away for 5 minutes

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
        owen_home = self.utils.is_entity_home(self.owen)
        allison_home = self.utils.is_entity_home(self.allison)
        work_time = (self.utils.is_entity_on(self.is_work_day) and
            self.now_is_between("07:45:00", "12:00:00") or
            self.now_is_between("13:00:00", "15:00:00"))

        if (not owen_home and not allison_home):
            self.log("Everyone away. Turning off all lights.")
            self.turn_on(self.all_off)
        elif (owen_home and not allison_home and work_time):
            self.log("Turning on day office lighting.")
            self.turn_on(self.day_office)