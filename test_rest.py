import algebra 
import rest_api_server
import math

def test_area_circle():
    area = algebra.area_circle(100)
    assert math.isclose(area, 31415.926535897932)

