import hassapi as hass

"""
Automation to restart the modem if we don't have internet.
"""
class Internet(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.internet_up = self.args["internet_up"]
        self.internet_modem_smart_plug = self.args["internet_modem_smart_plug"]
        # self.internet_router_smart_plug = self.args["internet_router_smart_plug"]

        # Restarts modem when no internet is detected for 1.5 minutes. Ping
        # checks if we have internet access every minute, so this time
        # allows for a second check to happen and confirm that we have no
        # internet access.
        self.listen_state(self.restart_modem, self.internet_up, new = "off", duration = 90)

    """
    Restarts modem smart plug. Then, sets a callback to check if the internet
    is up in 5 minutes or restarts router.
    """
    def restart_modem(self, entity, attribute, old, new, kwargs):
        self.restart_entity(self.internet_modem_smart_plug)

        # Router smart plug needs to be running a non-wifi based protocol
        # (like Zigbee) or we won't be able to turn it back on when the router
        # is off. I'm leaving this here until I get a smart plug that isn't
        # wifi based.
        # self.run_in(self.restart_router, 330) # Restart router if internet still down in 5.5 minutes.

    """
    Restarts router smart plug.
    """
    # def restart_router(self, cb_args):
    #     if (not self.utils.is_entity_on(self.internet_up)):
    #         self.restart_entity(self.internet_router_smart_plug)

    """
    Restarts input entity by turning it off and then scheduling a callback to
    run in 15 seconds to turn the entity back on.
    """
    def restart_entity(self, entity):
        if (self.utils.recently_triggered(entity, 300)):
            self.log("{} already manually restarted. Not restarting.".format(entity))
            return

        self.log("Restarting {}".format(entity))
        self.turn_off(entity)
        self.run_in(self.turn_on_entity, 15, entity = entity)

    """
    Turns input entity back on.
    """
    def turn_on_entity(self, kwargs):
        entity = kwargs["entity"]

        self.turn_on(entity)
        self.notify("Restarted {} due to internet outage.".format(entity))