from flask import Flask, jsonify, request
import requests
from mlAlgos import getCropRecommendation, getSoilParamsRecommendation, getRainfallLevelValues, getStateBasedItemPrices
import json

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
        'tamil nadu':	'11.059821,78.387451',
        'madhya pradesh':	'23.473324,77.947998',
        'haryana':	'29.238478,76.431885',
        'maharashtra':	'19.601194,75.552979',
        'tripura':	'23.745127,91.746826',
        'karnataka':	'15.317277,75.713890',
        'kerala':	'10.850516,76.271080',
        'uttar pradesh':	'28.207609,79.826660',
        'assam':	'26.244156,92.537842',
        'west bengal':	'22.978624,87.747803',
        'gujarat':	'22.309425,72.136230',
        'rajasthan':	'27.391277,73.432617',
        'punjab': '31.1471,75.3412',
        'manipur': '24.6637,93.9063',
        'meghalaya': '25.4670,91.3662',
        'andaman and nicobar': '10.7449,92.5000'
    }
    latlong = state_to_latlong[state]
    apiKey = 'a3d4d1fd09d84e57b4290807231102'
    URL = f'http://api.weatherapi.com/v1/current.json?key={apiKey}&q={latlong}&aqi=no'
    data = json.loads(requests.get(URL).text)
    temp = float(data["current"]["temp_c"])
    humidity = float(data["current"]["humidity"])
    return temp, humidity


def get_crop_suggestion_from_params(N, P, K, pH, temp, humidity):
    '''
    N, P, K, pH, temp, humidity --> crop list
    '''
    return getCropRecommendation(N=N, P=P, K=K, ph=pH, temperature=temp, humidity=humidity)


def get_soil_params_from_params(temp, humidity, crop):
    '''
    temp, humidity, crop --> N, P, K, pH
    '''
    return getSoilParamsRecommendation(temperature=temp, humidity=humidity, crop=crop)


def get_rainfall_timeseries_from_params(state, month: int):
    '''
    state, month (0 to 11) --> (rain in mm, year) list
    '''
    return getRainfallLevelValues(state=state, month=month)


def get_crop_prices_from_params(state):
    '''
    state --> (crop, selling price) list
    '''
    return getStateBasedItemPrices(state=state)

# ---- API Endpoints Definition ----


@app.route('/crop_suggestion', methods=['GET'])
def get_crop_suggestion():
    '''
    N, P, K, pH, state --> best crop
    '''
    N = float(request.args.get('N'))
    P = float(request.args.get('P'))
    K = float(request.args.get('K'))
    pH = float(request.args.get('pH'))
    state = request.args.get('state')
    temp, humidity = get_loc_info_from_state(state)
    best_crops = get_crop_suggestion_from_params(N, P, K, pH, temp, humidity)
    return jsonify(
        {
            'best_crops': best_crops
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
    res = get_soil_params_from_params(temp, humidity, crop)
    return jsonify(
        {
            'N': res['N'],
            'P': res['P'],
            'K': res['K'],
            'pH': res['pH']
        }
    )


@app.route('/rainfall_timeseries_data', methods=['GET'])
def get_rainfall_timeseries_data():
    '''
    state, month --> rainfall time series
    '''
    month = int(request.args.get('month'))
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
    price_list = get_crop_prices_from_params(state)
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
