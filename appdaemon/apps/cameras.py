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
        self.cameras = self.args["cameras"]
        self.owen = self.args["owen"]
        self.proximity_allison = self.args["proximity_allison"]
        self.proximity_owen = self.args["proximity_owen"]

        self.listen_state(self.turn_off_cameras, self.allison, new = "home")
        self.listen_state(self.turn_off_cameras, self.owen, new = "home")
        self.listen_state(self.turn_on_cameras, self.proximity_allison, new = 30)
        self.listen_state(self.turn_on_cameras, self.proximity_owen, new = 30)

    """
    Turns on the cameras if nobody is home and the triggered is moving away.
    """
    def turn_on_cameras(self, entity, attribute, old, new, kwargs):
        direction = self.get_state(entity, attribute="dir_of_travel")
        if direction != "towards" or self.someone_home():
            return
        
        self.turn_off_on_cameras(True)

    """
    Turns off the cameras if someone is home.
    """
    def turn_off_cameras(self, entity, attribute, old, new, kwargs):
        if not self.someone_home():
            return

        self.turn_off_on_cameras(False)

    """
    Turns off cameras if anyone home and cameras are on.
    Turns on cameras if everyone away from home and cameras are off.
    """
    def turn_off_on_cameras(self, turn_on: bool):
        camera_state_log_message = "on" if turn_on else "off"

        cameras_updated = False
        self.log("Turning {} cameras due to occcupancy.".format(camera_state_log_message))
        for camera in self.cameras:
            cameras_updated = self.turn_off_on_camera(camera, turn_on) or cameras_updated

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

    """
    If someone is actively home.
    """
    def someone_home(self) -> bool:
        return self.utils.is_entity_home(self.allison) or self.utils.is_entity_home(self.owen)