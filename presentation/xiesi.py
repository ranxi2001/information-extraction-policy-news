
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def complet():
    return jsonify({
        'text': "福州市城区水系联排联调中心副主任陈永锋介绍，福州市运用大数据、物联网、云计算等多种手段，建成城市级水系科学调度系统，",
    })
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=999)