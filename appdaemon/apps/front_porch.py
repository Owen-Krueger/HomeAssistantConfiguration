import hassapi as hass
import datetime

"""
Front porch automations.
"""
class FrontPorch(hass.Hass):
    
    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.default_time = datetime.time(22, 0, 0)
        self.allison = self.args["allison"]
        self.owen = self.args["owen"]
        self.porch_off_time = self.args["porch_off_time"]
        self.should_override_time = self.args["should_override_time"]
        self.front_porch_switch = self.args["front_porch_switch"]
        self.proximity_allison = self.args["proximity_allison"]
        self.proximity_owen = self.args["proximity_owen"]

        self.run_at_sunset(self.turn_on_front_porch, offset = datetime.timedelta(minutes =- 45).total_seconds()) # Turn lights on 45 minutes before sunset.
        self.handle = self.run_daily(self.turn_off_front_porch_time_based, self.utils.get_time(self.porch_off_time))
        self.listen_state(self.on_porch_off_time_change, self.porch_off_time, duration = 30) # Only update the next execution time when time has been set for 30 seconds.
        self.listen_state(self.on_override_boolean_turned_off, self.should_override_time, new = "off", duration = 30) # Only check if execution time needs defaulting when boolean has been off for 30 seconds.
        self.listen_state(self.turn_on_front_porch_location_based, self.proximity_owen, 
            old = lambda x : int(x) > 5,
            new = lambda x : int(x) <= 5) # When getting close to home.
        self.listen_state(self.turn_on_front_porch_location_based, self.proximity_allison, 
            old = lambda x : int(x) > 5,
            new = lambda x : int(x) <= 5) # When getting close to home.
        self.listen_state(self.turn_off_front_porch_location_based, self.allison, new = "home", duration = 300) # When home for 5 minutes.
        self.listen_state(self.turn_off_front_porch_location_based, self.owen, new = "home", duration = 300) # When home for 5 minutes.

    """
    On time change, cancel the timer and re-set it up so it executes
    at the new time. Sets override boolean if necessary.
    """
    def on_porch_off_time_change(self, entity, attribute, old, new, kwargs):
        self.log("Setting new execution time: {}".format(new))
        self.cancel_timer(self.handle)
        self.handle = self.run_daily(self.turn_off_front_porch_time_based, new)

        # If the override time, but the boolean wasn't turned on, turn on the boolean. Only set if time wasn't set to default.
        if (not self.utils.is_entity_on(self.should_override_time) and self.utils.get_time(self.porch_off_time) != self.default_time):
            self.log("Override boolean off but should be on. Turning on.")
            self.set_state(self.should_override_time, state = "on")

    """
    On override boolean changed, check if turned off. If turned off, reset
    the execution time to the default time of 10:00 PM.
    """
    def on_override_boolean_turned_off(self, entity, attribute, old, new, kwargs):
        self.log("Override turned off. Resetting time to 10:00 PM")
        self.set_state(self.porch_off_time, state=self.default_time)

    """
    Turns on the front porch lights if they are off.
    """
    def turn_on_front_porch(self, kwargs):
        if not self.utils.is_entity_on(self.front_porch_switch):
            self.log("Turning porch lights on.")
            self.turn_on(self.front_porch_switch)

    """
    Turns on porch if someone is close to home, lights are off, and it's late at
    night.
    """
    def turn_on_front_porch_location_based(self, entity, attribute, old, new, kwargs):
        if self.is_late() and not self.utils.is_entity_on(self.front_porch_switch):
            self.log("Turning on front porch lights due to someone getting close to home at night.")
            self.turn_on_front_porch()

    """
    Turns off the front porch lights if they are on and nobody is close to
    getting home.
    """
    def turn_off_front_porch_time_based(self, kwargs):
        if self.someone_close_to_home():
            self.log("Someone getting close to home. Not turning off front porch lights.")
            return

        if self.utils.is_entity_on(self.front_porch_switch):
            self.log("Turning off front porch lights.")
            self.turn_off_front_porch()

    """
    Turns off front porch lights if they're on, someone just got home, and it's
    late at night.
    """
    def turn_off_front_porch_location_based(self, entity, attribute, old, new, kwargs):
        if self.is_late() and self.utils.is_entity_on(self.front_porch_switch):
            self.log("Turning off front porch lights, due to lights being on and someone getting home late at night.")
            self.turn_off_front_porch()

    """
    Turns off the front porch lights if they are on.
    Will also reset the execution time for future runs if time was
    overridden for this run.
    """
    def turn_off_front_porch(self):
        self.turn_off(self.front_porch_switch)

        if self.utils.is_entity_on(self.should_override_time):
            self.log("Time overriden. Resetting execution time to default.")
            self.set_state(self.should_override_time, state="off")
            self.set_state(self.porch_off_time, state = self.default_time)
        pass

    """
    Returns if someone is close to home.
    """
    def someone_close_to_home(self):
        allison_close = self.utils.close_to_home(self.proximity_allison)
        owen_close = self.utils.close_to_home(self.proximity_owen)

        return allison_close or owen_close

    """
    Returns if it's late (but not too late...)
    """
    def is_late(self) -> bool:
        return self.now_is_between("22:00:00", "01:00:00")
