import hassapi as hass

class Laundry(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        should_notify = self.get_state(self.args["should_notify"])

        if (should_notify == "on"):
            self.set_up_load_listeners() # Sets up listener for washer and dryer load completion.

        self.listen_state(self.on_should_notify_changed, self.args["should_notify"])

    """
    Sets up listeners for washer and dryer finishing.
    """
    def set_up_load_listeners(self):
        self.washer_handler = self.listen_state(self.notify_both_users, self.args["washer"], new = "finish")
        self.dryer_handler = self.listen_state(self.notify_both_users, self.args["dryer"], new = "finished")

    """
    On should notify boolean change, cancel listeners if they're active and
    re-set them up if users should be notified on load completion.
    """
    def on_should_notify_changed(self, entity, attribute, old, new, kwargs):
        self.log('Notifications changed: {}'.format(new))

        if (old == "on"): # Cancel old listeners if they were active. 
            self.cancel_listen_state(self.washer_handler)
            self.cancel_listen_state(self.dryer_handler)

        if (new == "on"):
            self.set_up_load_listeners()

    """
    Attempts to notify users about load being complete.
    If nobody is home, it sets a flag to notify the first person that gets home.
    """
    def notify_both_users(self, entity, attribute, old, new, kwargs):
        device = "washer" if entity == self.args["washer"] else "dryer"
        message = "The {} has completed!".format(device)
        self.log("Notifying users that {} has completed.".format(device))

        owen_home = self.get_state(self.args["owen"]) == "home"
        allison_home = self.get_state(self.args["allison"]) == "home"

        if (not owen_home and not allison_home):
            self.log('Nobody home. Sending notification to both.')
            owen_home = True
            allison_home = True
        
        if (owen_home):
            self.notify(message, name="owen")

        if (allison_home):
            self.notify(message, name="allison")