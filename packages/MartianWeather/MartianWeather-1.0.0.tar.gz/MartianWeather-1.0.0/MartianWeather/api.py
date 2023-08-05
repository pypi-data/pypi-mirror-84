import requests

class Api:
    # Main API class
    def __init__(self, key):
        self._url    = 'https://api.nasa.gov/insight_weather/'
        self._params = {'api_key':key, 'feedtype':'json', 'ver':'1.0'}
        self._req    = requests.get(self._url, params=self._params)
        self._req.raise_for_status()

    @property
    def status(self):
        # Returns the status code of the request
        return self._req.status_code

    @property
    def json(self):
        # Returns a json object with data from the request
        return self._req.text

    @property
    def data(self):
        # Returns a python dict with data from the request
        return self._req.json()

    @property
    def available_sols(self):
        #A list of all available sols
        return self.data['sol_keys']

    @property
    def hours_required(self):
        #The number of hours with readings required to pass Nasa's validity checks
        return self.data['validity_checks']['sol_hours_required']

    @property
    def validity_checks(self):
        #A list all sols that have undergone validity checks
        #This doesn't mean that all measurements in said sol
        #have passed the checks
        return self.data['validity_checks']['sols_checked']

    @property
    def requests_limit(self):
        # The max amount of requests allowed for the current api key
        return int(self._req.headers['X-RateLimit-Limit'])

    @property
    def requests_remaining(self):
        # The remaining number of requests for the current api key
        return int(self._req.headers['X-RateLimit-Remaining'])
