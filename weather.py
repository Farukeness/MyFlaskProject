import requests
import datetime

def bilgilerigetir(city_name="Istanbul"):
    url2 = "http://api.weatherapi.com/v1/forecast.json?key=960e29f573d94fb7826195738232509&q={}&days=3&aqi=no&alerts=no"
    asilresponse = requests.get(url2.format(city_name)).json()
    info = {
        "city" : asilresponse["location"]["name"],
        "temp1" : asilresponse["forecast"]["forecastday"][0]["day"]["maxtemp_c"],
        "temp_icon" : asilresponse["forecast"]["forecastday"][0]["day"]["condition"]["icon"],
        "temp2" : asilresponse["forecast"]["forecastday"][1]["day"]["maxtemp_c"],
        "temp_icon2" : asilresponse["forecast"]["forecastday"][1]["day"]["condition"]["icon"],
        "temp3" :asilresponse["forecast"]["forecastday"][2]["day"]["maxtemp_c"],
        "temp_icon3" : asilresponse["forecast"]["forecastday"][2]["day"]["condition"]["icon"],
        "night_temp" : asilresponse["forecast"]["forecastday"][0]["day"]["mintemp_c"],
        "day_temp" : asilresponse["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
    }

    
    return info

def day_to_turkish(days):
    days_turkish = ["Pazartesi","Salı","Çarşamba","Peşembe","Cuma","Cumartesi","Pazar"]
    days_english = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    for day in range(len(days)):
        for x in range(len(days_english)):
            if days[day] == days_english[x]:
                days[day] = days_turkish[x]
    return days



today = datetime.date.today().strftime("%A")
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
next_day  = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%A")
days = [today,tomorrow,next_day]
days = day_to_turkish(days)




