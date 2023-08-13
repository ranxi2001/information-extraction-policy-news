from flask import Flask, request, jsonify
from paddlenlp import Taskflow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# 在这里定义你想要识别的实体类型
# UIE具有zero-shot能力，所以类型可以随便定义，但是识别的好坏不一定
schema = ['政策', '政府机构', '省份','城市地点','人名','人的代称','事件工程项目','会议','法规条例','组织机构企业','新闻杂志融媒体','国家']
# 第一运行时，联网状态下会自动下载模型
# device_id为gpu id，如果写-1则使用cpu,如果写0则使用gpu
# ie = Taskflow('information_extraction', schema=schema, device_id=0,task_path='./doccano/uie/checkpoint/model_best/')
ie = Taskflow('information_extraction', schema=schema, device_id=0,task_path='./uie-model/checkpoint/model_best3800')

def convert(result):
    result = result[0]
    formatted_result = []
    for label, ents in result.items():
        for ent in ents:
            formatted_result.append(
                {
                    "label": label,
                    "start_offset": ent['start'],
                    "end_offset": ent['end']
                })

    return formatted_result


@app.route('/', methods=['POST'])
def get_result():
    text = request.json['text']
    print(text)
    result = ie(text)
    formatted_result = convert(result)

    return jsonify(formatted_result)


if __name__ == '__main__':
	# 这里写端口的时候一定要注意不要与已有的端口冲突
	# 这里的host并不是说访问的时候一定要写0.0.0.0，但是这里代码要写0.0.0.0，代表可以被本网络中所有的看到
	# 如果是其他机器访问你创建的服务，访问的时候要写你的ip
    app.run(host='0.0.0.0', port=88)
