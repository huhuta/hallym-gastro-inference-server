import requests
import io
import numpy as np
from flask import Flask, request
from PIL import Image
from flask_cors import CORS
from flask import jsonify


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return 'inference request server home'


@app.route('/infer/<model>', methods=['POST'])
def infer_request(model):
    image_file = request.files['filepond']
    fileobj = image_file.read()

    list_data = decode_img_to_list(fileobj)
    response = ask_serving(list_data, model)

    if response.get('error', None):
        return jsonify(response)

    formatted_responses = response['predictions'].pop(0)
    return jsonify(formatted_responses)


def decode_img_to_list(fileobj):
    return np.array(Image.open(
        io.BytesIO(fileobj))).astype(
        dtype=np.float32).tolist()


def ask_serving(data, model):
    json = {
        'instances': data
    }
    print('http://{}-serving-svc/v1/models/{}:predict'.format(model, model))
    r = requests.post(
        'http://{}-serving-svc/v1/models/{}:predict'.format(model, model),
        json=json)
    return r.json()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
