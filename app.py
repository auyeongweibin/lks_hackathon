from flask import Flask, request
from flask_cors import CORS
import requests
from config import SEARCH_URL, GET_RESOURCE

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
    resource_url = GET_RESOURCE
    res = requests.get(url).json()
    docs = res['docs']
    if len(docs) == 0:
        return {'Message': 'Sorry we could not find any related resources'}
    result = [
        {
            'type': d['pnx']['display']['type'][0],
            'title': d['pnx']['display']['title'][0],
            'publisher': d['pnx']['display']['publisher'][0],
            'description': d['pnx']['display']['description'][0] if d['pnx']['display'].get('description') else '',
            'link': requests.post(resource_url.replace('[insert_id_here]', d['pnx']['control']['recordid'][0]), data=d).url,
            'summary': ''
        } for d in docs
    ]
    # TODO: Get Summary
    # TODO: Get Link
    return {'Resources': result}

if __name__ == "__main__":
    app.run()
