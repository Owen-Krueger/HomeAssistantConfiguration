import hassapi as hass

"""
Automation to let Owen know when he's home, but not on Wifi.
"""
class OwenPhoneWifi(hass.Hass):
    
    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.owen = self.args["owen"]
        self.phone_network = self.args["phone_network"]

        self.listen_state(self.notify_owen, self.owen, new = "home", duration = 1800) # When home for 30 minutes
        self.listen_state(self.notify_owen, self.phone_network, new = "cellular", duration = 1800) # When on cellular data for 30 minutes

    """
    Notifies Owen if he's at home without Wifi on.
    """
    def notify_owen(self, entity, attribute, old, new, kwargs):
        if (self.utils.is_entity_home(self.owen) and self.get_state(self.phone_network) == "cellular"):
            self.log("Notifying Owen that he's home with cellular on.")
            self.notify("Your phone is currently connected to cellular data", name = "owen")