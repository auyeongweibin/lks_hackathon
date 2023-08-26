from flask import Flask, request
from flask_cors import CORS
import requests
from config import SEARCH_URL, GET_RESOURCE

def get_url(doc):
    resource_url = GET_RESOURCE
    url = ''
    r =requests.post(resource_url.replace('[insert_id_here]', doc['pnx']['control']['recordid'][0]), json={'doc':doc})
    if r.status_code == 200:
        url = r.json().get("redirect_to")
    return url


def create_app(config_filename):
    application = app = Flask(__name__, static_url_path='')
    application.config.from_object(config_filename)
    cors = CORS(application, resources={r"/*": {"origins": "*"}})

    return application

app = create_app("config")

@app.route('/', methods=['GET'])

def index():
    return 'LKS Hackathon API Running...'

@app.route('/search', methods=['GET'])

def search():
    key = request.args.get('key')
    search_key = key.replace(' ', '+')
    url = SEARCH_URL.replace('[insert_search_here]', search_key)
    res = requests.get(url).json()
    docs = res['docs']
    if len(docs) == 0:
        return {'Message': 'Sorry we could not find any related resources'}
    result = [
        {
            'type': d['pnx']['display']['type'][0] if d['pnx']['display'].get('type') else '',
            'title': d['pnx']['display']['title'][0] if d['pnx']['display'].get('title') else '',
            'publisher': d['pnx']['display']['publisher'][0] if d['pnx']['display'].get('publisher') else '',
            'description': d['pnx']['display']['description'][0] if d['pnx']['display'].get('description') else '',
            'link': get_url(d),
            'summary': ''
        } for d in docs
    ]
    # TODO: Get Summary
    return {'Resources': result}

if __name__ == "__main__":
    app.run()