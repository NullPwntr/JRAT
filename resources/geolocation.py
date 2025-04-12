import requests, json

def get_geo_data():
    response = requests.get("http://ip-api.com/json/")

    if response.status_code == 200:
        data = json.loads(response.text)
        geodata = {}

        if data['status'] == "success":
            geodata["country"] = data["country"]
            geodata["country_code"] = data["countryCode"]
            geodata["region"] = data["regionName"]
            geodata["city"] = data["city"]
            geodata["zip"] = data["zip"]
            geodata["latitude"] = data["lat"]
            geodata["longitude"] = data["lon"]
            geodata["timezone"] = data["timezone"]
            geodata["isp"] = data["isp"]
            geodata["as"] = data["as"]
            geodata["ip"] = data["query"]

            return geodata, "success"
        else:
            return {}, "fail"
    else:
        return {}, "fail"