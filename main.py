from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
from util import get_infer_request_by_model_name, decode_img_to_list


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

    make_infer_request = get_infer_request_by_model_name(model)
    response = make_infer_request(list_data)

    if response.get('error', None):
        return jsonify(response)

    formatted_responses = response['predictions'].pop(0)
    return jsonify(formatted_responses)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
