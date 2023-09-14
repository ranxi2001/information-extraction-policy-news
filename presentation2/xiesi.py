
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def complet():
    text = request.json['text']
    return jsonify({
        'text': "实现“多水合一，网厂河一体化”的管理机制，统筹负责城区水系管理与调度指挥，实现防洪、排涝、调水、污水治理一中心统管。",
        'all': text+'实现“多水合一，网厂河一体化”的管理机制，统筹负责城区水系管理与调度指挥，实现防洪、排涝、调水、污水治理一中心统管。'
    })
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=999)