import json
import unittest
import datetime
import calendar

with open("./data-1.json", "r", encoding="utf-8") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r", encoding="utf-8") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)

_LOCATION_KEYS = ("country", "city", "area", "factory", "section")

def _iso_to_epoch_ms(iso_string):
    dt = datetime.datetime.strptime(iso_string.rstrip("Z"), "%Y-%m-%dT%H:%M:%S.%f")
    epoch_seconds = calendar.timegm(dt.timetuple())
    return epoch_seconds * 1000 + dt.microsecond // 1000

def convertFromFormat1(jsonObject):
    location_parts = jsonObject["location"].split("/")
    return {
        "deviceID":   jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp":  jsonObject["timestamp"],
        "location":   dict(zip(_LOCATION_KEYS, location_parts)),
        "data": {
            "status":      jsonObject["operationStatus"],
            "temperature": jsonObject["temp"],
        },
    }

def convertFromFormat2(jsonObject):
    return {
        "deviceID":   jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp":  _iso_to_epoch_ms(jsonObject["timestamp"]),
        "location":   {key: jsonObject[key] for key in _LOCATION_KEYS},
        "data": {
            "status":      jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"],
        },
    }

def main(jsonObject):
    if "device" in jsonObject:
        return convertFromFormat2(jsonObject)
    return convertFromFormat1(jsonObject)

class TestSolution(unittest.TestCase):
    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, "Converting from Type 1 failed")

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, "Converting from Type 2 failed")

if __name__ == "__main__":
    unittest.main(verbosity=2)
