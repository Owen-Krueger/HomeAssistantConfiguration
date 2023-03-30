import hassapi as hass

"""
Laundry automations.
"""
class Laundry(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.should_notify = self.args["should_notify"]
        self.washer = self.args["washer"]
        self.dryer = self.args["dryer"]
        self.allison_home = self.utils.is_entity_home(self.args["allison"])
        self.owen_home = self.utils.is_entity_home(self.args["owen"])

        if self.utils.is_entity_on(self.should_notify):
            self.set_up_triggers() # Sets up listener for washer and dryer load completion.

        self.listen_state(self.on_should_notify_change, self.should_notify, duration = 30) # Only update the automation triggers when boolean has been set for 30 seconds.

    """
    Sets up triggers for washer and dryer finishing.
    """
    def set_up_triggers(self):
        self.washer_handler = self.listen_state(self.notify_users, self.washer, new = "finish")
        self.dryer_handler = self.listen_state(self.notify_users, self.dryer, new = "finished")

    """
    On should notify boolean change, cancel listeners if they're active and
    re-set them up if users should be notified on load completion.
    """
    def on_should_notify_change(self, entity, attribute, old, new, kwargs):
        self.log("Notifications changed: {}".format(new))

        if old == "on": # Cancel old listeners if they were active. 
            self.cancel_listen_state(self.washer_handler)
            self.cancel_listen_state(self.dryer_handler)

        if new == "on":
            self.set_up_triggers()

    """
    Attempts to notify users about load being complete.
    If nobody is home, notifies both users.
    """
    def notify_users(self, entity, attribute, old, new, kwargs):
        device = "washer" if entity == self.washer else "dryer"
        message = "The {} has completed!".format(device)
        self.log("Notifying users that {} has completed.".format(device))

        if (not self.owen_home and not self.allison_home):
            self.log("Nobody home. Sending notification to both.")
            self.owen_home = True
            self.allison_home = True
        
        if (self.owen_home):
            self.notify(message, name="owen")

        if (self.allison_home):
            self.notify(message, name="allison")