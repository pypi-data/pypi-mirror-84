def get_sols(data):
    # Return a list of Sol instances
    sols = []
    for key in data['sol_keys']:
        sols.append(Sol(data, key))
    return sols

class Sol:
    # Class containing data from one Sol(Martian Day)
    def __init__(self, data, sol_key):
        self._key  = sol_key
        self._data = data

    @property
    def key(self):
        # The sol number
        return self._key

    @property
    def season(self):
        # Current season on mars
        return self._data[self._key]['Season']

    @property
    def first_utc(self):
        # Date and time(UTC) of the first collected datum
        return self._data[self._key]['First_UTC']

    @property
    def last_utc(self):
        # Date and time(UTC) of the last collected datum
        return self._data[self._key]['Last_UTC']

    @property
    def temp(self):
        # Temperature reading
        return Temp(self._data, self._key)

    @property
    def pressure(self):
        # Pressure reading
        return Pressure(self._data, self._key)

    @property
    def wind_speed(self):
        # Wind speed reading
        return WindSpeed(self._data, self._key)

    @property
    def wind_dir(self):
        # Wind direction readings
        return WindCompass(self._data, self._key)

class Measurement:
    # Parent class for all measurements
    def __init__(self, data, sol_key, type):
        self._valid = data['validity_checks'][sol_key][type]['valid']
        self._hours_with_data = data['validity_checks'][sol_key][type]['sol_hours_with_data']

    @property
    def valid(self):
        # Boolean value indicating if the data has passed Nasa's validity checks
        return self._valid

    @property
    def hours_with_data(self):
        # List which hours the samples are taken from
        return self._hours_with_data

class Sensor(Measurement):
    # Parent class for Temperature, Pressure and Wind speed
    def __init__(self, data, sol_key, type):
        super().__init__(data, sol_key, type)
        self._type=type

        try:
            self._min   = data[sol_key][type]['mn']
            self._max   = data[sol_key][type]['mx']
            self._avg   = data[sol_key][type]['av']
            self._count = data[sol_key][type]['ct']
        except KeyError:
            self._min   = None
            self._max   = None
            self._avg   = None
            self._count = None

    @property
    def min(self):
        # The sample with the lowest value
        return self._min

    @property
    def max(self):
        # The sample with the highest value
        return self._max

    @property
    def avg(self):
        # The average value of all samples
        return self._avg

    @property
    def count(self):
        # The number of samples taken by the sensor
        return self._count

    @property
    def unit(self):
        # The unit of the measurement
        return self._unit

class Temp(Sensor):
    def __init__(self, data, sol_key):
        super().__init__(data, sol_key, type='AT')
        self._unit = 'Celcius'

class Pressure(Sensor):
    def __init__(self, data, sol_key):
        super().__init__(data, sol_key, type='PRE')
        self._unit = 'Pascal'

class WindSpeed(Sensor):
    def __init__(self, data, sol_key):
        super().__init__(data, sol_key, type='HWS')
        self._unit = 'm/s'

class WindCompass(Measurement):
    # Wind Compass containing 16 compass points
    def __init__(self, data, sol_key):
        super().__init__(data, sol_key, type='WD')
        self._data   = data[sol_key]['WD']
        self._common = None

        # I don't mind these being hard coded seeing as count is the only
        # only variable subject to change (Please don't yell at me)
        self._dirs = [['N',0], ['NNE',22.5], ['NE',45], ['ENE',67.5],
                      ['E',90],['ESE',112.5],['SE',135],['SSE',157.5],
                      ['S',180],['SSW',202.5],['SW',225],['WSW',247.5],
                      ['W',270],['WNW',292.5],['NW',315],['NNW',337.5]]
        self._vectors = [(0.0, 1.0), (0.382683432365, 0.923879532511),
                        (0.707106781187, 0.707106781187), (0.923879532511, 0.382683432365),
                        (1.0, 0.0), (0.923879532511, -0.382683432365),
                        (0.707106781187, -0.707106781187), (0.382683432365, -0.923879532511),
                        (0.0, -1.0), (-0.382683432365, -0.923879532511),
                        (-0.707106781187, -0.707106781187), (-0.923879532511, -0.382683432365),
                        (-1.0, -0.0), (-0.923879532511, 0.382683432365),
                        (-0.707106781187, 0.707106781187), (-0.382683432365, 0.923879532511)]

        self._sensors = []
        for i in range(16):
            try:
                if self._dirs[i][0] == self._data['most_common']['compass_point']:
                    self._common = self.CompassPoint(self._data, str(i), self._dirs[i][0], self._dirs[i][1], self._vectors[i])
            except TypeError:
                self._common = self.CompassPoint(self._data, str(i), None, None, (None, None))
            self._sensors.append(self.CompassPoint(self._data, str(i), self._dirs[i][0], self._dirs[i][1], self._vectors[i]))

    @property
    def sensors(self):
        # A list of all 16 sensor objects in the wind compass
        return self._sensors
    @property
    def common(self):
        # The sensor with the most samples taken
        return self._common

    class CompassPoint():
        # Wind Direction Points
        def __init__(self, data, id, point, degrees, vector):
            self._degrees = degrees
            self._point   = point
            self._vector  = vector
            try:
                self._count  = data[id]['ct']
            except KeyError:
                self._count  = 0

        @property
        def degrees(self):
            # The angle of the sensor in degrees
            return self._degrees

        @property
        def point(self):
            # The heading of the sensor
            return self._point

        @property
        def vector(self):
            # A tuple containing the x and y values of the unit vector
            return self._vector

        @property
        def count(self):
            # The number of samples taken by the sensor
            return self._count
