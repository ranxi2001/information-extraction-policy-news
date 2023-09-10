from flask import Flask, request, jsonify
#coding=utf-8
from pprint import pprint
from flask_cors import CORS
from uie_predictor import UIEPredictor
app = Flask(__name__)
CORS(app)
# 在这里定义你想要识别的实体类型
# 实体类型 人名、人的代称、政策、法规条例、事件工程项目、会议
schema = [{"人名": "身份"},{'人的代称':"隶属"},{'政策':"发布单位"},{'政策':"针对群体"},{'法规条例':"发布单位"},{'法规条例':"针对群体"},{'事件工程项目':"发布单位"},{'事件工程项目':"针对群体"},{'会议':"发言人"},{'会议':"发布内容"},{'会议':"开会地点"},
          '政府机构', '省份','城市地点','组织机构企业','新闻杂志融媒体','国家']

# 设定抽取目标和定制化模型权重路径
my_ie = UIEPredictor(model='uie-base',task_path='/app/export',schema=schema,max_seq_len=512,device='cpu',engine='onnx')

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
                    'probability': float(value['probability']),
                    'hasRelati on': 1 if 'relations' in value else 0
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
    #按start值进行排序
    nodes = sorted(nodes, key=lambda x: x['start'])
    links = sorted(links, key=lambda x: x['source'])
    return jsonify({
        'nodes': nodes,
        'links': links
    })


if __name__ == '__main__':
    pprint(my_ie("新华社记者燕雁摄3月22日至25日，中共中央总书记、国家主席、中央军委主席习近平在福建考察。"))
    app.run(host='0.0.0.0', port=888)
