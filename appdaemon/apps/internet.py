import hassapi as hass

"""
Automation to restart the modem if we don't have internet.
"""
class Internet(hass.Hass):

    """
    Sets up the automation.
    """
    async def initialize(self):
        self.utils = self.get_app("utils")
        self.internet_up = self.args["internet_up"]
        self.restart_modem_script = self.args["restart_modem_script"]
        self.internet_modem_smart_plug = self.args["internet_modem_smart_plug"]
        self.internet_router_smart_plug = self.args["internet_router_smart_plug"]

        # Restarts modem when no internet is detected for 5.5 minutes. Ping
        # checks if we have internet access every 5 minutes, so this time
        # allows for a second check to happen and confirm that we have no
        # internet access.
        self.listen_state(self.restart_modem, self.internet_up, new = "off", duration = 33)

    """
    Restarts modem smart plug. Then, sets a callback to check if the internet
    is up in 5 minutes or restarts router.
    """
    async def restart_modem(self, entity, attribute, old, new, kwargs):
        await self.restart_entity(self.internet_modem_smart_plug)

        self.run_in(self.restart_router, 33) # Restart router if internet still down in 5.5 minutes.

    """
    Restarts router smart plug.
    """
    async def restart_router(self, cb_args):
        if (not self.utils.is_entity_on(self.internet_up)):
            await self.restart_entity(self.internet_router_smart_plug)

    """
    Restarts the input entity and notifies Owen.
    """
    async def restart_entity(self, entity):
        if (self.utils.recently_triggered(entity, 30)):
            self.log("{} already manually restarted. Not restarting.".format(entity))
            return

        self.log("Restarting {}".format(entity))
        self.turn_off(entity)
        await self.sleep(15)
        self.turn_on(entity)
        self.notify("Restarted {} due to internet outage.".format(entity))