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
        self.cameras = self.args["cameras"]

        self.listen_state(self.turn_off_on_cameras, self.allison, new = "home")
        self.listen_state(self.turn_off_on_cameras, self.owen, new = "home")
        self.listen_state(self.turn_off_on_cameras, self.allison, new = "not_home", duration = 10) # When away for 10 minutes.
        self.listen_state(self.turn_off_on_cameras, self.owen, new = "not_home", duration = 10) # When away for 10 minutes.

    """
    Turns off cameras if anyone home and cameras are on.
    Turns on cameras if everyone away from home and cameras are off.
    """
    def turn_off_on_cameras(self, entity, attribute, old, new, kwargs):
        owen_home = self.utils.is_entity_home(self.owen)
        allison_home = self.utils.is_entity_home(self.allison)
        someone_home = owen_home or allison_home
        camera_state_log_message = "off" if someone_home else "on"

        cameras_updated = False
        self.log("Turning {} cameras due to occcupancy.".format(camera_state_log_message))
        for camera in self.cameras:
            cameras_updated = self.turn_off_on_camera(camera, not someone_home) or cameras_updated

        if cameras_updated:
            self.notify("Cameras turned {}.".format(camera_state_log_message), name="owen")

    """
    Turns off or on the camera, depending on input and current state.
    """
    def turn_off_on_camera(self, entity, turn_on: bool) -> bool:
        if turn_on and not self.utils.is_entity_on(entity):
            self.turn_on(entity)
            return True
        elif not turn_on and self.utils.is_entity_on(entity):
            self.turn_off(entity)
            return True
        
        return False