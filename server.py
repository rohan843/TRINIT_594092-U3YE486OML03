from flask import Flask, jsonify

FLASK_PORT = 4002

app = Flask(__name__)

# ---- API Endpoints Definition ----
@app.route('/user_game_rec', methods=['GET'])
def get_user_game_recs():
    return jsonify(
        {
        }
    )

@app.route('/refresh_model_data', methods=['POST'])
def refresh_model_data():
    return jsonify(
        {
        }
    )


# ---- Error Handlers ----
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(
        {
        }
    )


if __name__ == '__main__':
    app.run(
        port=FLASK_PORT
    )
