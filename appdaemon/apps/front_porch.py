import hassapi as hass
import datetime

class FrontPorch(hass.Hass):
    
    """
    Sets up the automation.
    """
    def initialize(self):
        time = self.parse_time(self.get_state(self.args["time"]))

        self.run_at_sunset(self.turn_on_front_porch, offset = datetime.timedelta(minutes =- 45).total_seconds())
        self.handle = self.run_daily(self.turn_off_front_porch, time)
        self.listen_state(self.on_override_time_changed, self.args["time"], duration = 60) # Only update the next execution time when time has been set for 60 seconds.

    """
    On time change, cancel the timer and re-set it up so it executes
    at the new time.
    """
    def on_override_time_changed(self, entity, attribute, old, new, kwargs):
        self.log('Setting new execution time: {}'.format(new))
        self.cancel_timer(self.handle)
        self.handle = self.run_daily(self.turn_off_front_porch, new)

    """
    Turns on the front porch lights if they are off.
    """
    def turn_on_front_porch(self, kwargs):
        if self.get_state(self.args["switch"]) == "off":
            self.log('Turning porch lights on.')
            self.turn_on(self.args["switch"])

    """
    Turns off the front porch lights if they are on.
    Will also reset the execution time for future runs if time was
    overridden for this run.
    """
    def turn_off_front_porch(self, kwargs):
        if self.get_state(self.args["switch"]) == "on":
            self.log('Turning porch lights off.')
            self.turn_off(self.args["switch"])

        if self.get_state(self.args["boolean"]):
            self.log('Time overriden. Resetting execution time to default.')
            self.set_state(self.args["boolean"], state="off")
            self.set_state(self.args["time"], state=datetime.time(22, 0, 0))
