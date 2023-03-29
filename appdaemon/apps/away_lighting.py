import hassapi as hass

class AwayLighting(hass.Hass):
    
    def initialize(self):

        if (self.args["boolean"] == "on"): # Only run automations if boolean is on
            self.run_daily(self.away_lighting, "08:30:00")
            self.listen_state(self.away_lighting, self.args["allison"], duration = 300) # When away for 5 minutes
            self.listen_state(self.away_lighting, self.args["owen"], duration = 300) # When away for 5 minutes

    """
    Checks who is home. If everyone is gone, all lights are turned off.
    If only Allison is gone and Owen is at work, turn on office lighting.
    """
    def away_lighting(self, entity, attribute, old, new, kwargs):
        owen_home = self.get_state(self.args["owen"]) == "home"
        allison_home = self.get_state(self.args["allison"]) == "home"
        work_time = (self.get_state("is_workday") == "on" and
            self.now_is_between("08:00:00", "12:00:00") or
            self.now_is_between("13:00:00", "15:00:00"))

        if (not owen_home and not allison_home):
            self.log("Everyone away. Turning off all lights")
            self.turn_on(self.args["all_off"])
            return
        elif (owen_home and not allison_home and work_time):
            self.log("Turning on day office lighting.")
            self.turn_on(self.args["day_office"])