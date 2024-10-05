from flask import Flask, request, jsonify
import datetime as dt
import meteomatics.api as api

app = Flask(__name__)

def get_filtered_weather_data(lat, lon):
    coords = [(lat, lon)]
    username = 'amaljyothicollegeofengineering_tom_aaron'
    password = 'A561xfaMS4'
    parameters = ['heavy_rain_warning_24h:idx', 'precip_24h:mm', 'tstorm_warning_24h:idx']
    model = 'mix'
    startdate = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
    enddate = startdate + dt.timedelta(days=10)
    interval = dt.timedelta(hours=24)

    df = api.query_time_series(coords, startdate, enddate, interval, parameters, username, password, model=model)
    
    filtered_df = df[(df['heavy_rain_warning_24h:idx'] > 1) | (df['tstorm_warning_24h:idx'] > 2)]
    return filtered_df if not filtered_df.empty else None
    # return df

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON format"}), 400
    lat = data.get('lat')
    lon = data.get('lon')
    # lat, lon = 25.29, 91.58
    # hostel = 9.53, 76.82
    result = get_filtered_weather_data(lat, lon)
    if result is not None:
        # return jsonify(result.to_dict())
        return jsonify({
            "message": "Heavy rainfall or thunderstorm warnings found.",
            "info": "Get cover"    
        })
    else:
        return jsonify({
            "message": "No heavy rainfall or thunderstorm warnings found.",
            "info": "All Good bro"
        })

if __name__ == '__main__':
    app.run(debug=True)