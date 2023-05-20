import requests


def getweather(city):
    print(f"Getting weather info for {city}")

    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = base_url + "q=" + city + "&appid=" + '38631b309820b90d5361500061f0f065'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = format(main['temp'] - 273.15, '.2f')
        humidity = main['humidity']
        pressure = main['pressure']
        report = data['weather']
        final_report = f"Weather of {city.upper()}\nTemperature: {temperature}℃\nHumidity: {humidity}\nPressure: {format(pressure * 0.1, '.2f')} kPa\nWeather Report: {report[0]['description']}😪 "
        return final_report
    else:
        return "Enter a valid City name\n'/weather city'"
