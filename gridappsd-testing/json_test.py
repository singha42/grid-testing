import json
import pytest
a = {"data": [{"Diffuse": 23.5682655, "AvgWindSpeed": 9.9208, "TowerRH": 50.7, "long": "105.18 W", "MST": "15:00", "TowerDryBulbTemp": 74.822, "DATE": "7/14/2013", "DirectCH1": 74.4836898, "GlobalCM22": 81.34333290000001, "AvgWindDirection": 338.5, "time": 1373814000, "place": "Solar Radiation Research Laboratory", "lat": "39.74 N"}, {"Diffuse": 23.417767499999997, "AvgWindSpeed": 7.8584, "TowerRH": 52.32, "long": "105.18 W", "MST": "15:01", "TowerDryBulbTemp": 75.038, "DATE": "7/14/2013", "DirectCH1": 74.1650428, "GlobalCM22": 80.6234508, "AvgWindDirection": 343.2, "time": 1373814060, "place": "Solar Radiation Research Laboratory", "lat": "39.74 N"}], "responseComplete": True, "id": "1112398614"}

print(a["data"][0])
assert 'lat' in a["data"][0]

sensor_query = {"queryMeasurement": "gridappsd-sensor-simulator","queryFilter": {"simulation_id": "582881157"},"responseFormat": "JSON"}
print(json.loads(sensor_query))
print(sensor_query["queryFilter"]["simulation_id"])

