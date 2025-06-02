from mbta_api import *
import api_info

# API Access Information
username = api_info.USERNAME
api_key = api_info.MBTA_KEY

mbta_api = MBTA_API(api_key, username)
mbta_results = MBTA_Results(subway_routes="subway_routes.json")

# Q1: Get all subway routes
subway_routes = mbta_api.response_to_json(mbta_api.get_subway_routes())
mbta_results.print_subway_route_names()



