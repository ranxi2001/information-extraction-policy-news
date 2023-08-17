from flask import Flask, request, jsonify
from paddlenlp import Taskflow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# 在这里定义你想要识别的实体类型
schema = [{"人名": "身份"},{'人的代称':"隶属"},{'政策':"发布单位"},{'政策':"针对群体"},{'法规条例':"发布单位"},{'法规条例':"针对群体"},{'事件工程项目':"发布单位"},{'事件工程项目':"针对群体"},{'会议':"发言人"},{'会议':"发布内容"},{'会议':"开会地点"},
          '政府机构', '省份','城市地点','组织机构企业','新闻杂志融媒体','国家']

# 设定抽取目标和定制化模型权重路径
my_ie = Taskflow("information_extraction", schema=schema, task_path='uie-model/checkpoint/model_best4000')

@app.route('/', methods=['POST'])
def process_text():
    text = request.json['text']
    results = my_ie(text)
    nodes = []
    links = []
    for result in results:  # 遍历列表中的每个字典
        for key, values in result.items():  # 在每个字典上调用items()
            for value in values:
                nodes.append({
                    'id': value['start'],
                    'label': key,
                    'text':value['text'],
                    'start': value['start'],
                    'end': value['end'],
                    'probability': value['probability']
                })
                if 'relations' in value:
                    for relation_type, related_entities in value['relations'].items():
                        for related_entity in related_entities:
                            links.append({
                                'source': value['start'],
                                'target': related_entity['start'],
                                'sourceText': value['text'],
                                'sourceLabel': key,
                                'targetText': related_entity['text'],
                                'relation': relation_type
                            })
    return jsonify({
        'nodes': nodes,
        'links': links
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=888)
