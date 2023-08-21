import hassapi as hass

"""
Automations to ping entities if they become unavailable.
"""
class PingEntities(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")

        for entity in self.args["dictionary"]:
            self.listen_state(self.ping_entity, entity["entity"], new = "unavailable", ping = entity["ping"], sync_entity = entity.get("sync_entity", None))

    """
    Pings the entity and then waits 5 seconds to see if it comes online.
    """
    def ping_entity(self, entity, attribute, old, new, kwargs):
        message = "Pinging {} because it's unavailable".format(entity)
        self.log(message)
        self.notify(message, name = "owen")

        self.call_service("button/press", entity_id = kwargs["ping"])
        self.run_in(self.ensure_entity_on, 5, entity = entity, sync_entity = kwargs["sync_entity"])

    """
    Checks if the entity has stopped being unavailable. If `sync_entity` provided,
    sync the state of this entity to be the state of `sync_entity`. This is useful
    if one of two lamps goes unavaliable. This should get it online and set to
    the expected state.
    """
    def ensure_entity_on(self, kwargs):
        entity = kwargs["entity"]
        sync_entity = kwargs["sync_entity"]

        if self.get_state(entity) == "unavailable":
            self.log("{} pinged but still unavailable".format(entity))
            return

        if sync_entity != None:
            self.utils.sync_entities(sync_entity, entity)
