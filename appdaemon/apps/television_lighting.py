import hassapi as hass

"""
Turns on downstairs lights on if downstairs TV on or living room lamps if
upstairs TV is on.
"""
class TelevisionLighting(hass.Hass):
    
    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.downstairs_lights = self.args["downstairs_lights"]
        self.downstairs_tv_on = self.args["downstairs_tv_on"]
        self.living_room_automations_on = self.args["living_room_automations_on"]
        self.living_room_lamps = self.args["living_room_lamps"]
        self.upstairs_tv_on = self.args["upstairs_tv_on"]

        if self.utils.is_entity_on(self.living_room_automations_on):
            self.set_up_triggers() # Sets up listeners for TV statuses

        self.listen_state(self.on_boolean_change, self.living_room_automations_on, duration = 30) # Only update the automation triggers when boolean is set for 30 seconds.

    """
    Sets up triggers for downstairs and upstairs TVs.
    """
    def set_up_triggers(self):
        self.downstairs_tv_on_handler = self.listen_state(self.turn_on_lights, self.downstairs_tv_on, new = "on")
        self.upstairs_tv_on_handler = self.listen_state(self.turn_on_lights, self.upstairs_tv_on, new = "on")

    """
    On living room automations boolean change, cancel listeners if they're active and
    re-set them up if living room light should be automated
    """
    def on_boolean_change(self, entity, attribute, old, new, kwargs):
        self.log("Living room automations boolean changed: {}".format(new))

        if old == "on": # Cancel old listeners if they were active. 
            self.cancel_listen_state(self.downstairs_tv_on_handler)
            self.cancel_listen_state(self.upstairs_tv_on_handler)

        if new == "on":
            self.set_up_triggers()

    """
    Turn on lights depending on which TV is on.
    """
    def turn_on_lights(self, entity, attribute, old, new, kwargs):
        if not self.now_is_between("05:30:00", "21:00:00"): # So lights don't turn on while we're sleeping.
            self.log("{} on but it's late. Not turning lights on.".format(entity))
            return
        
        entity_to_turn_on = self.downstairs_lights if entity == self.downstairs_tv_on else self.living_room_lamps
        self.log("{} turned on. Turning on {}.".format(entity, entity_to_turn_on))

        if not self.utils.is_entity_on(entity_to_turn_on):
            self.turn_on(entity_to_turn_on)
        else:
            self.log("{} already on.".format(entity_to_turn_on))