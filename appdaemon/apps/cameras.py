import hassapi as hass

"""
Camera automation depending on people being home or not.
"""
class Cameras(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.allison = self.args["allison"]
        self.owen = self.args["owen"]
        self.cat_camera_up_smart_plug = self.args["cat_camera_up_smart_plug"]
        self.cat_camera_down_smart_plug = self.args["cat_camera_down_smart_plug"]

        self.listen_state(self.turn_off_on_cameras, self.allison, new = "home")
        self.listen_state(self.turn_off_on_cameras, self.owen, new = "home")
        self.listen_state(self.turn_off_on_cameras, self.allison, new = "not_home", duration = 600) # When away for 10 minutes.
        self.listen_state(self.turn_off_on_cameras, self.owen, new = "not_home", duration = 600) # When away for 10 minutes.

    """
    Turns off cameras if anyone home and cameras are on.
    Turns on cameras if everyone away from home and cameras are off.
    """
    def turn_off_on_cameras(self, entity, attribute, old, new, kwargs):
        cameras_on = self.utils.is_entity_on(self.cat_camera_up_smart_plug) or self.utils.is_entity_on(self.cat_camera_down_smart_plug)
        owen_home = self.utils.is_entity_home(self.owen)
        allison_home = self.utils.is_entity_home(self.allison)

        if ((owen_home or allison_home) and cameras_on):
            self.log("Turning off cameras due to someone getting home.")
            self.turn_off(self.cat_camera_up_smart_plug)
            self.turn_off(self.cat_camera_down_smart_plug)
            self.notify("Cameras turned off.", name="owen")
        elif ((not owen_home and not allison_home) and not cameras_on):
            self.log("Turning on cameras due to everyone being away.")
            self.turn_on(self.cat_camera_up_smart_plug)
            self.turn_on(self.cat_camera_down_smart_plug)
            self.notify("Cameras turned on.", name="owen")