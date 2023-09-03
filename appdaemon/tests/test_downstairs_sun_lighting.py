from unittest import mock
from appdaemon_testing.pytest import automation_fixture
from apps.downstairs_sun_lighting import DownstairsSunLighting

def test_callbacks_are_registered(hass_driver, downstairs_sun_lighting: DownstairsSunLighting):
    listen_state = hass_driver.get_mock("listen_state")
    listen_state.assert_any_call(
        downstairs_sun_lighting.set_downstairs_light_level, "light.downstairs_lights", new = "on", duration = 5
    )

def test_light_on_no_brightness_attribute(hass_driver, downstairs_sun_lighting: DownstairsSunLighting):
    hass_driver.set_state("light.downstairs_lights", "on")

    get_state = hass_driver.get_mock("get_state")
    assert get_state.call_count == 1
    get_state.assert_called_once_with(
        "light.downstairs_lights",
        attribute = "brightness"
    )
    set_state = hass_driver.get_mock("set_state")
    assert set_state.call_count == 0

def test_light_on_night(hass_driver, downstairs_sun_lighting: DownstairsSunLighting):
    with hass_driver.setup():
        hass_driver.set_state("light.downstairs_lights", 255, attribute_name="brightness")
        hass_driver.set_state("sun.sun", 5, attribute_name="elevation")

    hass_driver.set_state("light.downstairs_lights", "on")

    set_state = hass_driver.get_mock("set_state")
    assert set_state.call_count == 1
    set_state.assert_called_once_with(
        "light.downstairs_lights",
        state = "on",
        attributes = {"brightness": "128"}
    )

def test_light_on_day(hass_driver, downstairs_sun_lighting: DownstairsSunLighting):
    with hass_driver.setup():
        hass_driver.set_state("light.downstairs_lights", 128, attribute_name="brightness")
        hass_driver.set_state("sun.sun", 15, attribute_name="elevation")

    hass_driver.set_state("light.downstairs_lights", "on")

    set_state = hass_driver.get_mock("set_state")
    assert set_state.call_count == 1
    set_state.assert_called_once_with(
        "light.downstairs_lights",
        state = "on",
        attributes = {"brightness": "255"}
    )


@automation_fixture(
    DownstairsSunLighting,
    args={
        "downstairs_lights": "light.downstairs_lights",
        "sun": "sun.sun"
    }
)

def downstairs_sun_lighting() -> DownstairsSunLighting:
    pass