import requests
import io
import numpy as np
from PIL import Image


def decode_img_to_list(fileobj):
    return np.array(Image.open(
        io.BytesIO(fileobj))).astype(
        dtype=np.float32).tolist()


def get_infer_request_by_model_name(model):
    # TODO refacotr unused things
    port_selector = {
        '5class': 8501,
        'neoplasm': 8502,
        'cancer': 8503,
    }
    port = port_selector.get(model, None)

    def make_request(data):
        json = {
            'instances': data
        }
        print('http://{}-serving-svc/v1/models/{}:predict'.format(model, model))
        r = requests.post(
            'http://{}-serving-svc/v1/models/{}:predict'.format(model, model),
            json=json)
        return r.json()
    return make_request
