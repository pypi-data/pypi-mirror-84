import requests

class Weather:
    
    def __init__(self):
        res = requests.get("http://api.openweathermap.org/data/2.5/find", 
        params={
            'q': 'Moscow,RU',
            'type': 'like',
            'units': 'metric',
            'APPID': 'a40a7ba874dd59960768cd44d9f3ced7'
        })
        self.data = res.json()

    def get_description(self):
        return(self.data['list'][1]['weather'][0]['description'])

    def get_temp(self):
        return(self.data['list'][1]['main']['temp'])
    
    def get_wind_speed(self):
        return(self.data['list'][1]['wind']['speed'])

    def get_wind_deg(self):
        return(self.data['list'][1]['wind']['deg'])

    def get_pressure(self):
        return(self.data['list'][1]['main']['pressure'])
    
    def get_humidity(self):
        return(self.data['list'][1]['main']['humidity'])

    def get_feels_like(self):
        return(self.data['list'][1]['main']['feels_like'])