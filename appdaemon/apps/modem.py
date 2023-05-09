import hassapi as hass

"""
Automation to restart the modem if we don't have internet.
"""
class Modem(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.internet_up = self.args["internet_up"]
        self.restart_modem_script = self.args["restart_modem_script"]
        self.internet_modem_smart_plug = self.args["internet_modem_smart_plug"]

        # Restarts modem when no internet is detected for 5.5 minutes. Ping
        # checks if we have internet access every 5 minutes, so this time
        # allows for a second check to happen and confirm that we have no
        # internet access.
        self.listen_state(self.restart_modem, self.internet_up, new = "off", duration = 330)

    """
    Restarts the modem via the restart modem script.
    """
    def restart_modem(self, entity, attribute, old, new, kwargs):
        # Prevents the modem from being restarted if a user manually restarted
        # it recently.
        if self.utils.recently_triggered(self.internet_modem_smart_plug, 300):
            self.log("Modem already manually restarted. Not restarting.")
            return

        self.log("Restarting modem.")
        self.turn_on(self.restart_modem_script)
        self.notify("Restarted modem due to internet outage.", name = "owen")