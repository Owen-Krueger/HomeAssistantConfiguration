import hassapi as hass

class AwayLighting(hass.Hass):
    
    """
    Sets up the automation.
    """
    def initialize(self):
        self.should_turn_off_lights = self.args["should_turn_off_lights"]
        self.allison = self.args["allison"]
        self.owen = self.args["owen"]
        self.all_off = self.args["all_off"]
        self.day_office = self.args["day_office"]

        if (self.should_turn_off_lights == "on"): # Only run automations if boolean is on
            self.set_up_triggers()

        self.listen_state(self.on_automation_boolean_changed, self.should_turn_off_lights, duration = 60) # Only update the automation triggers when boolean has been set for 60 seconds.

    """
    Sets up triggers for presence and time triggers.
    """
    def set_up_triggers(self):
        self.office_time_handler = self.run_daily(self.away_lighting, "08:30:00")
        self.allison_presence_handler = self.listen_state(self.away_lighting, self.allison, duration = 300) # When away for 5 minutes
        self.owen_presence_handler = self.listen_state(self.away_lighting, self.owen, duration = 300) # When away for 5 minutes

    """
    On automation boolean change, cancel triggers if they're active and
    re-set them up if users should be notified on load completion.
    """
    def on_automation_boolean_changed(self, entity, attribute, old, new, kwargs):
        self.log('Automation turned {}'.format(new))

        if (old == "on"): # Cancel old triggers if they were active.
            self.cancel_timer(self.office_time_handler)
            self.cancel_listen_state(self.allison_presence_handler)
            self.cancel_listen_state(self.owen_presence_handler)

        if (new == "on"):
            self.set_up_triggers()

    """
    Checks who is home. If everyone is gone, all lights are turned off.
    If only Allison is gone and Owen is at work, turn on office lighting.
    """
    def away_lighting(self, entity, attribute, old, new, kwargs):
        owen_home = self.get_state(self.owen) == "home"
        allison_home = self.get_state(self.allison) == "home"
        work_time = (self.get_state("is_workday") == "on" and
            self.now_is_between("08:00:00", "12:00:00") or
            self.now_is_between("13:00:00", "15:00:00"))

        if (not owen_home and not allison_home):
            self.log("Everyone away. Turning off all lights")
            self.turn_on(self.all_off)
            return
        elif (owen_home and not allison_home and work_time):
            self.log("Turning on day office lighting.")
            self.turn_on(self.day_office)