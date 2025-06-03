# MBTA Routes

Uses the MBTA API to retrieve information about subway routes and subway stops.

## Setup/Installation
Libraries:
- `requests` - Making HTTP requests to the MBTA API.
- `json` - Parsing JSON responses from the API.
- `pandas` - Handling data in a more structured way.

The libraries can be installed via individual pip commands:
```bash
pip install requests json pandas
```
or via the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
```
## Usage

A separate local file, `api_info.py` should contain an `api_key` and a 
`username` for authentication with the MBTA API.

### Subway Routes

In `main.py`, `subway_routes()` will retrieve and print the names of all of the 
subway routes.

### Subway Route Information 

In `main.py`, `subway_stops_information()` will retrieve and print the name of
the route with the most stops, the route with the least stops, and a list of 
all stops that connect two or more subway routes.

### Traveling Between Routes

In `main.py`, `travel_between_stops(stop_1, stop_2)`, will retrieve and print
the names of the subway routes, in order, that connect the given stops.

### Testing

There are some unit tests in `test_mbta_api.py` that can be run via 
`pytest test_mbta_api.py` to verify the functionality of some of the helper 
and analysis functions.

## Resources
- [MBTA API Documentation](https://api-v3.mbta.com/docs/swagger/index.html)
- [Requests Documentation](https://requests.readthedocs.io/en/latest/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
