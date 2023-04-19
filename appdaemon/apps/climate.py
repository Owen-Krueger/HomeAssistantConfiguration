import hassapi as hass

"""
Climate automations
There are a few concepts that are tracked within this automation.

Time based temperature:
Within the HA UI, users can specify day time and night time, plus temperatures for
each time. This allows the house to be set to different temperatures during the day
and night. These temperatures will only be set if someone is currently at home. It
will keep track of what the temperature should be set to, so if someone gets home,
the house can be set to what it should be at.

Away temperature:
These automations contain two different location based temperatures. If everyone
is not at home for over an hour, but are all within 30 miles of home, the
temperature is set to the "short away" temperature. This temperature is a little
warmer or colder than the desired temperature, to save energy, but isn't a huge
deviation. This is so, when someone gets home, the house can quickly get back to
its desired temperature.

On the other hand, if everyone is away and gets more than 30 miles away from home,
the house assumes they're going to be away for a longer period of time or are on
a vacation. The house will then be set to the "long away" temperature, which is
significantly further away from the desired temperature, as nobody will be home
for a longer period of time. The automation will notify the users to verify that
they're actually going to be away for a longer period of time before switching to
this away temperature. The "long away" temperature can also be set if HA is
switched into vacation mode.

When the house is set to the "short away" temperature, it will set itself back to
the desired temperature when someone gets home. When the house is set to the "long
away" temperature, the house will set itself back to the desired temperature when
someone gets within 30 miles of the house or if HA is removed from vacation mode.
This is so there can be some time to get the house back to an acceptable
temperature before anyone gets home.

Away temperatures are accomplished by using offsets. Within the HA UI, users can set
the offset of how much the thermostat should deviate from desired when away for a
short period of time, and how much to deviate when away for a long period of time.
These offsets will take into account whether the system is currently set to heat or
cool to determine if the temperature should be raised or lowered.

For example: If away when the HVAC mode is set to heat, the temperature will be
lowered by the offset. If away when the HVAC mode is set to cool, the temperature
will be raised by the offset.

Temperature Deviations:

"""
class Climate(hass.Hass):

    """
    Sets up the automation.
    """
    def initialize(self):
        self.utils = self.get_app("utils")
        self.climate_automations = self.args["climate_automations"]
        self.climate_away_offset = int(self.args["climate_away_offset"])
        self.climate_day_start = self.args["climate_day_start"]
        self.climate_day_temp = int(self.args["climate_day_temp"])
        self.climate_thermostat = self.args["climate_thermostat"]
        self.climate_night_start = self.args["climate_night_start"]
        self.climate_night_temp = int(self.args["climate_night_temp"])
        self.climate_vacation_offset = int(self.args["climate_vacation_offset"])
        self.mode_vacation = self.args["mode_vacation"]
        self.owen = self.args["owen"]
        self.owen_proximity = self.args["owen_proximity"]

        self.is_heat_mode = self.get_state(self.climate_thermostat) == "heat"
        self.climate_desired_temp = self.climate_day_temp if self.now_is_between(self.utils.get_time(self.climate_day_start), self.utils.get_time(self.climate_night_start)) else self.climate_night_temp

        # Triggers that only are checked when climate automation boolean is on.
        if self.utils.is_entity_on(self.climate_automations):
            self.set_up_triggers()

        # Triggers that should always be checked, regardless of whether the
        # climate automation boolean is on or not.
        self.listen_state(self.on_climate_automations_change, self.climate_automations, duration = 30) # Only update the automation triggers when boolean has been set for 30 seconds.
        self.listen_event(self.set_vacation_mode, event='mobile_app_notification_action', action='climate_off')
        self.listen_state(self.check_climate_deviation, selef.climate_thermostat, attribute = 'current_temperature')

    """
    Sets up triggers for presence and time triggers.
    """
    def set_up_triggers(self):
        self.climate_day_start_handle = self.run_daily(self.set_time_based_temperature, self.climate_day_start, temperature = self.climate_day_temp)
        self.climate_night_start_handle = self.run_daily(self.set_time_based_temperature, self.climate_night_start, temperature = self.climate_night_temp)
        self.climate_vacation_handle = self.listen_state(self.set_vacation_mode, self.mode_vacation)
        self.allison_home_state_handle = self.listen_state(self.set_time_based_temperature, self.allison, new = "home", temperature = self.climate_desired_temp)
        self.owen_home_state_handle = self.listen_state(self.set_time_based_temperature, self.owen, new = "home", temperature = self.climate_desired_temp)
        self.allison_away_state_handle = self.listen_state(self.set_short_away_temperature, self.allison, new = "away", duration = 3600) # Only set away temp if away for an hour
        self.owen_away_state_handle = self.listen_state(self.set_short_away_temperature, self.owen, new = "away", duration = 3600) # Only set away temp if away for an hour
        self.hvac_mode_change_handle = self.listen_state(self.on_hvac_mode_change, self.climate_thermostat, duration = 30) # Only change HVAC mode if mode has been switched for 30 seconds

    """
    On automation boolean change, cancel triggers if they're active and
    re-set them up if they're currently disabled.
    """
    def on_climate_automations_change(self, entity, attribute, old, new, kwargs):
        self.log("Turning climate automation {}.".format(new))
        if old == "on":
            self.cancel_timer(self.climate_day_start_handle)
            self.cancel_timer(self.climate_night_start_handle)
            self.cancel_listen_state(self.climate_vacation_handle)
            self.cancel_listen_state(self.allison_home_state_handle)
            self.cancel_listen_state(self.owen_home_state_handle)
            self.cancel_listen_state(self.allison_away_state_handle)
            self.cancel_listen_state(self.owen_away_state_handle)

        if new == "on":
            self.set_up_triggers()

    """
    On HVAC mode change, update if we're currently in heat mode or not to use
    with offsets when away or on vacation.
    """
    def on_hvac_mode_change(self, entity, attribute, old, new, kwargs):
        self.log("HVAC mode switched to {}.".format(new))
        self.is_heat_mode = new == "heat"

    """
    Sets temperature based on it being the start of day or start of night.
    If nobody is home, temperature will not change, as it should already be set
    for being away from home.
    """
    def set_time_based_temperature(self, entity, attribute, old, new, kwargs):
        temperature = kwargs["temperature"]
        self.climate_desired_temp = int(temperature)
        if self.anyone_home():
            self.set_temperature(temperature)

    """
    Sets main thermostat to away temperature.
    """
    def set_short_away_temperature(self, entity, attribute, old, new, kwargs):
        if self.noone_home():
            self.set_temperature_with_offset(self.climate_away_offset)

    """
    Sets main thermostat to long away/vacation temperature if turned on.
    Sets back to desired temp if turned off.
    """
    def set_vacation_mode(self, entity, attribute, old, new, kwargs):
        self.log("Vacation mode turned {}.".format(new))
        if new == "on":
            self.set_temperature_with_offset(self.climate_vacation_offset)
        else:
            self.set_temperature(self.climate_desired_temp)

        # Turns off automations if in vacation mode turned on. Turns on
        # automations if vacation mode turned off.
        self.set_state(self.climate_automations, state = self.utils.get_opposite_state(new))

    """
    Sets the temperature to be the day temp + or - the offset.
    If mode is heat, subtract the offset.
    If mode is cool, add the offset.
    Example: Current Temp = 70 - Offset = 5
    Heat: 70 - 5 = 65
    Cool: 70 + 5 = 75
    """
    def set_temperature_with_offset(self, offset):
        if self.is_heat_mode:
            offset *= -1 # When in heat mode, we should lower the temperature by the offset, rather than raise it
        new_temperature = int(self.get_state(self.climate_desired_temp)) + offset
        self.set_temperature(new_temperature)


    """
    Sets main thermostat to inputted temperature.
    """
    def set_temperature(self, temperature):
        self.log("Setting temperature to {}".format(temperature))
        self.call_service(
            "climate/set_temperature",
            entity_id=self.climate_thermostat,
            temperature=temperature,
        )

    """

    """
    def check_climate_deviation(self, entity, attribute, old, new, kwargs):
        self.log("Notifying user of deviated temperature.")
        data = self.utils.get_json_from_file("climate_deviated")