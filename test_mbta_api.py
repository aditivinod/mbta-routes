"""
Test cases for the MBTA API requests, analysis, and results classes.
"""
import pytest
from mbta_api import *
import pandas as pd
import json


def test_save_json(tmp_path):
    """
    Test that saving JSON to a file actually works.
    """
    data = {"key": "value"}
    file_path = tmp_path / "test.json"
    save_json(data, file_path)

    with open(file_path, 'r') as f:
        loaded_data = json.load(f)

    assert loaded_data == data


def test_json_to_dataframe(tmp_path):
    """
    Test that converting JSON data to a DataFrame has the expected contents.
    """
    data = {"data": [{"key": "value1"}, {"key": "value2"}]}
    file_path = tmp_path / "test.json"

    with open(file_path, 'w') as f:
        json.dump(data, f)

    df = json_to_dataframe(file_path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 1)
    assert df['key'].tolist() == ['value1', 'value2']


routes = pd.DataFrame({
    "id": ["route1", "route2"],
    "name": ["Route 1", "Route 2"]
})

stops_routes = pd.DataFrame({
    "route_id": ["route1", "route1", "route2", "route2", "route2"],
    "stop_id": ["stop1", "stop2", "stop1", "stop2", "stop3"],
    # List of stops per route
    "stops": [["stop1", "stop2"], ["stop1", "stop2"], ["stop1", "stop2", "stop3"], ["stop1", "stop2", "stop3"], ["stop1", "stop2", "stop3"]],
    "attributes.long_name": ["Route 1", "Route 1", "Route 2", "Route 2", "Route 2"]
})


@pytest.fixture(params=[(routes, stops_routes)])
def mbta_analysis(request):
    """
    Create a MBA_Analsysis instance for testing.
    """
    routes, stops_routes = request.param
    return MBTA_Analysis(routes, stops_routes)


def test_get_max_stops(mbta_analysis):
    """
    Test that get_max_stops performs an accurate computation.
    """
    max_stops = mbta_analysis.get_max_stops()

    assert isinstance(max_stops, tuple)
    assert len(max_stops) == 2
    assert max_stops[0] == "Route 2"
    assert max_stops[1] == 3


def test_get_min_stops(mbta_analysis):
    """
    Test that get_min_stops performs an accurate computation.
    """
    min_stops = mbta_analysis.get_min_stops()

    assert isinstance(min_stops, tuple)
    assert len(min_stops) == 2
    assert min_stops[0] == "Route 1"
    assert min_stops[1] == 2
