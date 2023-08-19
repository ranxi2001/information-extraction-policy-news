from flask import Flask, request, jsonify
from paddlenlp import Taskflow


app = Flask(__name__)

# 在这里定义你想要识别的实体类型
# UIE具有zero-shot能力，所以类型可以随便定义，但是识别的好坏不一定
schema = [{"人名": "身份"},{'人的代称':"隶属"},{'政策':"发布单位"},{'政策':"针对群体"},{'法规条例':"发布单位"},{'法规条例':"针对群体"},{'事件工程项目':"发布单位"},{'事件工程项目':"针对群体"},{'会议':"发言人"},{'会议':"发布内容"},{'会议':"开会地点"},
          '政府机构', '省份','城市地点','组织机构企业','新闻杂志融媒体','国家']
# 第一运行时，联网状态下会自动下载模型
# device_id为gpu id，如果写-1则使用cpu,如果写0则使用gpu
# ie = Taskflow('information_extraction', schema=schema, device_id=0,task_path='./doccano/uie/checkpoint/model_best/')
ie = Taskflow('information_extraction', schema=schema, device_id=0, task_path='../uie-model/checkpoint/model_best4000')

@app.route('/', methods=['POST'])
def get_result():
    text = request.json['text']
    # print(text)
    result = ie(text)
    return result

if __name__ == '__main__':
	# 这里写端口的时候一定要注意不要与已有的端口冲突
	# 这里的host并不是说访问的时候一定要写0.0.0.0，但是这里代码要写0.0.0.0，代表可以被本网络中所有的看到
	# 如果是其他机器访问你创建的服务，访问的时候要写你的ip
    app.run(host='0.0.0.0', port=88)
