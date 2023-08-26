from flask import Flask, request
from flask_cors import CORS
import requests
from config import SEARCH_URL

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
    doc = res['docs']
    if len(doc) == 0:
        return {'Message': 'Sorry we could not find any related resources'}
    result = [
        {
            'type': d['pnx']['display']['type'],
            'title': d['pnx']['display']['title'],
            'creationdate': d['pnx']['display']['creationdate'] if d['pnx']['display'].get('creationdate') else '',
            'creator': d['pnx']['display']['creator'] if d['pnx']['display'].get('creator') else '',
            'publisher': d['pnx']['display']['publisher'],
            'description': d['pnx']['display']['description'] if d['pnx']['display'].get('description') else ''
        } for d in doc
    ]
    return {'Resources': result[0]}

if __name__ == "__main__":
    app.run()
