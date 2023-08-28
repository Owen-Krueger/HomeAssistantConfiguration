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
            self.listen_state(self.ping_entity, entity["entity"], new = "unavailable", ping = entity["ping"], sync_entity = entity.get("sync_entity", None), count = 1)

    """
    Wraps `ping_entity_inner`. This is called by `listen_state`.
    """
    def ping_entity(self, entity, attribute, old, new, kwargs):
        kwargs["entity"] = entity # Add entity to kwargs for inner method to use.
        self.ping_entity_inner(kwargs)

    """
    Pings the entity and waits 5 seconds to see if it comes online.
    """
    def ping_entity_inner(self, kwargs):
        self.log("Pinging {} because it's unavailable".format(kwargs["entity"]))

        self.call_service("button/press", entity_id = kwargs["ping"])
        self.run_in(self.ensure_entity_on, 5, kwargs) # Wait 5 seconds.

    """
    Checks if the entity has stopped being unavailable. If `sync_entity` provided,
    sync the state of this entity to be the state of `sync_entity`. This is useful
    if one of two lamps goes unavaliable. This should get it online and set to
    the expected state.
    """
    def ensure_entity_on(self, kwargs):
        entity = kwargs["entity"]
        count = kwargs["count"]

        if self.get_state(entity) == "unavailable": # Ping didn't fix state.
            self.log("{} pinged but still unavailable. (Count: {})".format(entity, count))

            if int(count) >= 3:
                self.notify("{} pinged multiple times but still unavailable.".format(entity), name = "owen")
                return
            
            new_count = str(int(count) +1)
            kwargs["count"] = new_count # Sets updated count to pass to `ping_entity_inner`.
            self.run_in(self.ping_entity_inner, 300, kwargs) # Wait 5 minutes.

        # If available, check if there's a second entity to sync state with.
        sync_entity = kwargs["sync_entity"]
        if sync_entity != None:
            self.utils.sync_entities(sync_entity, entity)
