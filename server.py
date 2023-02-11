from flask import Flask, jsonify, request

FLASK_PORT = 4002

app = Flask(__name__)

# ---- API Endpoints Definition ----


@app.route('/crop_suggestion', methods=['GET'])
def get_crop_suggestion():
    '''
    N, P, K, pH, state --> best crop
    '''
    return jsonify(
        {
        }
    )


@app.route('/soil_suggestion', methods=['GET'])
def get_soil_suggestion():
    '''
    state, crop --> optimal N, P, K, pH of soil values
    '''
    return jsonify(
        {
        }
    )


@app.route('/rainfall_timeseries_data', methods=['GET'])
def get_rainfall_timeseries_data():
    '''
    state, month --> rainfall time series
    '''
    return jsonify(
        {
        }
    )


@app.route('/crop_price_by_state_data', methods=['GET'])
def get_crop_price_by_state_data():
    '''
    state --> crop and their market prices
    '''
    return jsonify(
        {
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
