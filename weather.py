from flask import Flask,render_template,request,abort
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request
#import datetime for sunrise and sunset time
from datetime import datetime


app = Flask(__name__)
def tocelcius(temp):
    return str(round(float(temp) - 273.16,2))
def tofahrenheit(temp):
    temp_F = round(float(temp) - 273.16,2) * 1.8 + 32
    return str(round(temp_F,2))


@app.route('/',methods=['POST','GET'])
def weather():
    api_key = '37e2444e4a0e93d1a6aceefc13a78633'
    if request.method == 'POST':
        city = request.form['city']
    else:
        #for default name mathura
        city = 'Chennai'

    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    # converting json data to dictionary

    list_of_data = json.loads(source)
    sunrise = list_of_data['sys']['sunrise']
    ts1 = int(sunrise)
    sunrise_time = datetime.fromtimestamp(ts1).strftime('%d-%m-%y %H:%M')
    sunset = list_of_data['sys']['sunset']
    ts2 = int(sunset)
    sunset_time = datetime.fromtimestamp(ts2).strftime('%d-%m-%y %H:%M')

    # data for variable list_of_data 
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "cityname": str(city),
        "weather": str(list_of_data['weather'][0]['description']),
        "temp": tocelcius(list_of_data['main']['temp']) + ' °C' + ' / ' + tofahrenheit(list_of_data['main']['temp']) + ' °F',
        "feels_like": tocelcius(list_of_data['main']['feels_like']) + ' °C' + ' / ' + tofahrenheit(list_of_data['main']['feels_like']) + ' °F',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
        "max_temp": tocelcius(list_of_data['main']['temp_max']) + ' °C' + ' / ' + tofahrenheit(list_of_data['main']['temp_max']) + ' °F',
        "min_temp": tocelcius(list_of_data['main']['temp_min']) + ' °C' + ' / ' + tofahrenheit(list_of_data['main']['temp_min']) + ' °F',
        "sunrise": str(sunrise_time),
        "sunset": str(sunset_time)
    }
    return render_template('weather_index.html',data=data)



if __name__ == '__main__':
    app.run(debug=True)