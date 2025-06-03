from mbta_api import *
import api_info

# API Access Information
username = api_info.USERNAME
api_key = api_info.MBTA_KEY


# Setup
mbta_requests = MBTA_Requests(api_key, username)

routes_json = mbta_requests.get_subway_routes()
save_json(routes_json, "subway_routes.json")
routes = json_to_dataframe("subway_routes.json")

stops_routes_json = mbta_requests.pair_stops_and_routes(routes_json)
save_json(stops_routes_json, "stops_routes.json")
stops_routes = json_to_dataframe("stops_routes.json")

mbta_analysis = MBTA_Analysis(routes, stops_routes)
mbta_results = MBTA_Results(mbta_analysis)


# Q1: Get all subway routes
def subway_routes():
    mbta_results.print_subway_route_names()

# Q2: Get stop information for subway routes


def subway_stops_information():
    mbta_results.print_max_stops()
    mbta_results.print_min_stops()
    mbta_results.print_connected_stops()

# Q3: Travel between two subway stops


def travel_between_stops(stop_1, stop_2):
    mbta_results.print_connected_route(stop_1, stop_2)


def main():
    subway_routes()
    subway_stops_information()
    mbta_results.print_connected_route("Ashmont", "Arlington")


main()
