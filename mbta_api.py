"""
Interacts with the MBTA API to retrieve and handle information.
"""
import requests
import json
import pandas as pd

# General helper functions for converting & saving JSON data.
    
def save_json(response, filename):
    """
    Saves a response as a JSON file
    
    Args:
        response: The JSON to be saved as a file.
        filename: The name of the file to save the response to.
    """
    with open(filename, 'w') as json_file:
        json.dump(response, json_file, indent=4)

def json_to_dataframe(json_file):
    """
    Converts a JSON file to a pandas DataFrame.

    Args:
        json_file: The path to the JSON file to be converted.

    Returns:
        A pandas DataFrame containing the data from the JSON file.
    """
    with open(json_file, 'r') as file:
        data = json.load(file)
    return pd.json_normalize(data['data'])

class MBTA_Requests:
    """
    Interacts with the MBTA API.

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
            request: The request to give the MBTA API.

        Returns:
            The response from the MBTA API.
        """
        response = requests.get(f"{self.base_url}{request}", auth=self._auth)
        return response
                                
    def get_subway_routes(self):
        """
        Gets all subway routes from the MBTA API.

        Returns:
            A JSON containing all subway routes.
        """
        request = "routes?filter[type]=0,1"
        response = self.get_request(request)
        subway_routes = response.json()
        return subway_routes

    def get_stops_on_route(self, route):
        """
        Gets all the stops on a specific route.

        Args:
            route: A string representing the route ID to get the stops for.

        Returns: 
            A response from the MBTA API containing all the stops on the given
                route.
        """
        response = requests.get(f"{self.base_url}stops?filter[route]={route}", auth=self._auth)
        return response
    
    def pair_stops_and_routes(self, subway_routes):
        """
        Integrates subway stops into the JSON for their respective routes.

        Args: 
            subway_routes: A JSON containing subway routes

        Returns:
            A JSON containing the routes with all the stops data.
        """
        for route in subway_routes['data']:
            id = route['id']
            stops_response = self.get_stops_on_route(id)
            stops_data = stops_response.json()
            route['stops'] = stops_data['data']

        return subway_routes
    
    # UNUSED: Gets all routes from MBTA API
    def get_routes(self):
        """
        Gets all routes from the MBTA API.

        Returns:
            A response from the API containing all routes.
        """
        response = requests.get(f"{self.base_url}routes", auth=self._auth)
        return response

    # UNUSED: Gets all subway stops from MBTA API
    def get_subway_stops(self):
        """
        Fetches all stops for all subway routes.

        Args:
            route: The route to fetch the stops for.

        Returns:
            A response from the API containing all subway stops.
        """
        response = requests.get(f"{self.base_url}stops?filter[route_type]=0,1", auth=self._auth)
        return response

class MBTA_Results:
    """
    Outputs various results depending on information from the MBTA_Requests.

    Attributes:
        subway_routes: A DataFrame representing subway routes information.
        route_stop_pairs: A DataFrame representing subway routes & their stops.
    """
    def __init__(self, subway_routes, stops_routes):
        self.subway_routes = subway_routes  # Lowk worth removing entirely
        self.stops_routes = stops_routes
    
    def print_subway_route_names(self):
        """
        Prints the names of all MBTA subway routes.
        """
        print (self.subway_routes['attributes.long_name'].tolist())

    def get_max_stops(self):
        """
        Gets the name of the route with the maximum number of stops & the 
        number of stops.

        Returns: 
            A tuple containing a string representing the route name and an
            integer representing the number of stops on that route.
        """
        stop = self.stops_routes.loc[self.stops_routes['stops'].str.len().idxmax()]
        return stop['attributes.long_name'], len(stop['stops'])
    
    def get_min_stops(self):
        """
        Gets the name of the route with the minimum number of stops & the 
        number of stops.

        Returns: 
            A tuple containing a string representing the route name and an
            integer representing the number of stops on that route.
        """
        stop = self.stops_routes.loc[self.stops_routes['stops'].str.len().idxmin()]
        return stop['attributes.long_name'], len(stop['stops'])
    

    def get_connected_routes(self):
        """
        Gets the stops that connect two or more subway routes and the route 
        names for each stop.
        
        Returns:
            A list containing a string stop name and a list of string route 
            names that the stop is connected to.
        """
        counts = self.stops_routes.explode('stops')['stops'].value_counts()

        connected = (counts > 1).keys()
        connected_stops = []

        for stop in connected: 
            matching_routes = self.stops_routes[self.stops_routes['stops'].apply(lambda stops: stop in stops)]['attributes.long_name']
            connected_stops.append([stop['attributes']['name'], matching_routes.tolist()])
        
        return connected_stops

    def print_max_stops(self):
        """
        Prints the subway route with the maximum number of stops.
        """
        route, num_stops = self.get_max_stops()
        print(f"Max Stops: {route}, Count: {num_stops}.")

    def print_min_stops(self):
        """
        Prints the subway route with the minimum number of stops.
        """
        route, num_stops = self.get_min_stops()
        print(f"Min Stops: {route}, Count: {num_stops}.")

    def print_connected_stops(self):
        """
        Prints the stops that are connected between subway routes and their 
        corresponding routes.
        """
        connected_stops = self.get_connected_routes()
        for stop, routes in connected_stops:
            print(f"Stop: {stop}, Routes: {', '.join(routes)}.")

