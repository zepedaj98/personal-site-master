# -*- coding: utf-8 -*-
"""weather.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1injbIvhMCuZRxiTH8hLE9foQZ0MSvfmN
"""

from bs4 import BeautifulSoup as bs 
import requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)

    # create a new soup
    soup = bs(html.text, "html.parser")
    
    # store all results on this dictionary
    result = {}

    # extract region
    result['region'] = soup.find("span", attrs={"data-testid": "PresentationName"}).text
    #extract sunrise time 
    result['sunrise'] = soup.find("span", attrs={"data-testid": "SunriseTime"}).text
    #extract sunset time 
    result['sunset'] = soup.find("span", attrs={"data-testid": "SunsetTime"}).text
    # extract temperature now
    result['temp_now'] = soup.find("span", attrs={"data-testid": "TemperatureValue"}).text
    # get the day and hour now
    result['day'] = soup.find("div", attrs={"class": "DailyForecast--timestamp--22Azh"}).text
    # get the precipitation
    result['precipitation'] = soup.find("span", attrs={"data-testid":"precip", "data-testid": "PercentageValue"}).text
    # get the % of humidity
    result['humidity'] = soup.find("span", attrs={"class":"DetailsTable--value--2YD0-","data-testid": "PercentageValue"}).text
    # get the % of humidity
    result['UV'] = soup.find("span", attrs={"data-testid": "UVIndexValue"}).text
    # extract the wind
    result['wind'] = soup.find("span", attrs={"data-testid": "Wind"}).text
    # extract weather summary
    result['summary'] = soup.find("p", attrs={"data-testid": "wxPhrase"}).text

    next_days = []
    days = soup.find("h3", attrs={"class": "DetailsSummary--daypartName--kbngc"})
    for day in days.findAll("h3", attrs={"class": "DetailsSummary--daypartName--kbngc"}):
        # extract the name of the day
        day_name = day.findAll("h3")[0].attrs['daypartName']
      #  # get weather status for that day
       # weather = day.find("img").attrs["alt"]
       # temp = day.findAll("span", {"class": "wob_t"})
        # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
       # max_temp = temp[0].text
        # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
       # min_temp = temp[2].text
        #next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
        next_days.append({"name": day_name})
    # append to result
    result['next_days'] = next_days
    return result

if __name__ == "__main__":
    URL = "https://weather.com/weather/tenday/l/Albuquerque+NM?canonicalCityId=2defda56c5089a3cae25463d822f01e81fa91fcc68d08f190e404a38ae70a9f1"
    data = get_weather_data(URL)
    #Print weather data. 
    print( data["day"][6:])
    print(data["region"])
    print(data["temp_now"])
    print(data["summary"])
    print(data["wind"])
    print(data["UV"])
    print(data["humidity"])
    print(data["precipitation"])
    print(data["sunrise"])
    print(data["sunset"])
    print(data["next_days"])