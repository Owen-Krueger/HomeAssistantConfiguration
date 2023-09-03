from unittest import mock
from appdaemon_testing.pytest import automation_fixture
from apps.laundry import Laundry

def test_washer_finished(hass_driver, laundry: Laundry):
    hass_driver.set_state("sensor.washer_washer_job_state", "finish")

    notify = hass_driver.get_mock("notify")
    assert notify.call_count == 2
    message = "The washer has completed!"
    notify.assert_has_calls(
        [mock.call(message, name='owen'),
         mock.call(message, name='allison')]
    )

def test_dryer_finished(hass_driver, laundry: Laundry):
    hass_driver.set_state("sensor.dryer_dryer_job_state", "finished")

    notify = hass_driver.get_mock("notify")
    assert notify.call_count == 2
    message = "The dryer has completed!"
    notify.assert_has_calls(
        [mock.call(message, name='owen'),
         mock.call(message, name='allison')]
    )

@automation_fixture(
    Laundry,
    args={
        "dryer": "sensor.dryer_dryer_job_state",
        "washer": "sensor.washer_washer_job_state"
    }
)

def laundry() -> Laundry:
    pass