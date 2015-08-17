# Weather

This is a python based program, parse weather forcast data from ![中央氣象局-開放資料平臺](http://opendata.cwb.gov.tw/)

## Basic Usage

Get latest temperature data in a 臺南
```
from weather import Weather, WeatherObservation
forcast = WeatherObservation()

forcast.get_column_data_by_country('臺南', 'TEMP')
```

Get all available country in a report
```
from weather import Weather, WeatherObservation
forcast = WeatherObservation()

for country in forcast.show_avail_country():
    print country
```
