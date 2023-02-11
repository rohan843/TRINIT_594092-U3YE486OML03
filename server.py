from flask import Flask, jsonify, request
import requests

FLASK_PORT = 4002

app = Flask(__name__)

# TODO: Remove rainfall

# ---- Utility Functions ----


def get_loc_info_from_state(state):
    '''
    state --> temp, humidity
    '''
    temp = ''
    humidity = ''
    state_to_latlong = {
        'Tamil Nadu':	'11.059821,78.387451',
        'Telangana':	'17.123184,79.208824',
        'Madhya Pradesh':	'23.473324,77.947998',
        'Haryana':	'29.238478,76.431885',
        'Chhattisgarh':	'21.295132,81.828232',
        'Haryana':	'29.065773,76.040497',
        'Madhya Pradesh':	'25.794033,78.116531',
        'Maharashtra':	'19.601194,75.552979',
        'Tripura':	'23.745127,91.746826',
        'Telangana':	'17.874857,78.100815',
        'Karnataka':	'15.317277,75.713890',
        'Kerala':	'10.850516,76.271080',
        'Uttar Pradesh':	'28.207609,79.826660',
        'Assam':	'26.244156,92.537842',
        'Maharashtra':	'19.663280,75.300293',
        'Tamil Nadu':	'11.127123,78.656891',
        'Karnataka':	'15.317277,75.713890',
        'West Bengal':	'22.978624,87.747803',
        'Gujarat':	'22.309425,72.136230',
        'Odisha':	'20.940920,84.803467',
        'Rajasthan':	'27.391277,73.432617',
        'Himachal Pradesh':	'32.084206,77.571167'
    }
    latlong = state_to_latlong[state]
    apiKey = 'a3d4d1fd09d84e57b4290807231102'
    URL = f'http://api.weatherapi.com/v1/current.json?key={apiKey}&q={latlong}&aqi=no'
    data = requests.get(URL).text
    temp = str(data["current"]["temp_c"])
    humidity = str(data["current"]["humidity"])
    return temp, humidity


def get_crop_suggestion_from_params(N, P, K, pH, temp, humidity):
    '''
    N, P, K, pH, temp, humidity --> best crop
    '''


def get_soil_params_from_params(temp, humidity, crop):
    '''
    temp, humidity, crop --> N, P, K, pH
    '''

def get_rainfall_timeseries_from_params(state, month):
    '''
    state, month --> (rain in mms, year) list
    '''

def get_crop_proces_from_params(state):
    '''
    state --> (crop, selling price) list
    '''

# ---- API Endpoints Definition ----


@app.route('/crop_suggestion', methods=['GET'])
def get_crop_suggestion():
    '''
    N, P, K, pH, state --> best crop
    '''
    N = request.args.get('N')
    P = request.args.get('P')
    K = request.args.get('K')
    pH = request.args.get('pH')
    state = request.args.get('state')
    temp, humidity = get_loc_info_from_state(state)
    best_crop = get_crop_suggestion_from_params(N, P, K, pH, temp, humidity)
    return jsonify(
        {
            'best_crop': best_crop
        }
    )


@app.route('/soil_suggestion', methods=['GET'])
def get_soil_suggestion():
    '''
    state, crop --> optimal N, P, K, pH of soil values
    '''
    crop = request.args.get('crop')
    state = request.args.get('state')
    temp, humidity = get_loc_info_from_state(state)
    N, P, K, pH = get_soil_params_from_params(temp, humidity, crop)
    return jsonify(
        {
            'N': N,
            'P': P,
            'K': K,
            'pH': pH
        }
    )


@app.route('/rainfall_timeseries_data', methods=['GET'])
def get_rainfall_timeseries_data():
    '''
    state, month --> rainfall time series
    '''
    month = request.args.get('month')
    state = request.args.get('state')
    time_ser = get_rainfall_timeseries_from_params(state, month)
    return jsonify(
        {
            'timeseries_data': time_ser
        }
    )


@app.route('/crop_price_by_state_data', methods=['GET'])
def get_crop_price_by_state_data():
    '''
    state --> crop and their market prices
    '''
    state = request.args.get('state')
    price_list = get_crop_proces_from_params(state)
    return jsonify(
        {
            'price_data': price_list
        }
    )


# ---- Error Handlers ----
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(
        {
            'message': 'The requested endpoint was not found.'
        }
    )


if __name__ == '__main__':
    app.run(
        port=FLASK_PORT
    )
