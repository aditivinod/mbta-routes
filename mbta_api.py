"""
Interacts with the MBTA API to retrieve and handle information.
"""
import requests
import json

class MBTA_API:
    """
    Interacts with the MBTA.

    Attributes:
        _api_key: A string representing the authentication key for the MBTA API.
        _auth: A tuple containing the username and authentication key for the
            MBTA API.
        base_url: A string representing the base URL for the MBTA API.
    """
    def __init__(self, api_key, username):
        self._api_key = api_key
        self._auth = (username, self._api_key)
        self.base_url = 'https://api-v3.mbta.com/'

    def get_request(self, request):
        """
        Gets a response from the MBTA API.

        Args:
            request: The specific request to give the API.

        Returns:
            The response from the API.
        """
        response = requests.get(f"{self.base_url}{request}", auth=self._auth)
        return response

    def get_routes(self):
        """
        Gets all routes from the MBTA API.

        Returns:
            A dictionary containing all routes.
        """
        response = requests.get(f"{self.base_url}routes", auth=self._auth)
        return response
                                
    def get_subway_routes(self):
        """
        Gets all subway routes from the MBTA API.

        Returns:
            A dictionary from the API containing subway routes
        """
        response = requests.get(f"{self.base_url}routes?filter[type]=0,1", auth=self._auth)
        return response
    
    def response_to_json(self, response, filename="subway_routes.json"):
        """
        Saves a request as a JSON file
        
        Args:
            response: The response from the API to be saved.
            filename: The name of the file to save the response to.
        """
        with open(filename, "w") as json_file:
            json.dump(response.json(), json_file, indent=4)

class MBTA_Results:
    """
    Retrieves results from the MBTA API.

    Attributes:
        subway_routes: A dictionary representing subway routes information.
    """
    def __init__(self, subway_routes):
        if subway_routes.endswith('.json'):
            self.subway_routes = json.load(open(subway_routes, 'r'))
    
    def print_subway_route_names(self):
        """
        Prints the names of all MBTA subway routes.
        """
        for route in self.subway_routes['data']:
            print(f"{route['attributes']['long_name']}, ")

