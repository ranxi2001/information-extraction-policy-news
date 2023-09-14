from flask import Flask, request, jsonify
from paddlenlp import Taskflow
from flask_cors import CORS
from neo4j import GraphDatabase
class Example:
    def __init__(self):
        self.driver = None
        self.session = None

    def connect(self, uri, auth,):
        self.driver = GraphDatabase.driver(uri, auth=auth)
        # default_session = self.driver.session()
        # default_session.run("create database example;")
        # default_session.close()
        self.session = self.driver.session(database="demo")

    def create_graph(self,nodes,links):
        for node in nodes:
            self.create_node(node)
        for link in links:
            self.create_link(link)
    def create_node(self,node):
        query = f"CREATE (p:{node['label']} {{id:$id, text: $text, hasRelation:$hasRelation}})"
        self.session.run(query, id=node['id'], text=node['text'], hasRelation=node['hasRelation'])
    def create_link(self,link):
        query = f"MATCH (a:{link['sourceLabel']}),(b:{link['targetLabel']})\nWHERE a.text = $sourceText AND b.text = $targetText AND a.id = $source AND b.id = $target\nCREATE (a)-[r:{link['relation']}]->(b)"
        self.session.run(query, sourceText=link['sourceText'], targetText=link['targetText'], source=link['source'], target=link['target'])
    def delete_graph(self):
        self.session.run("drop database example;")
    def disconnect(self):
        self.session.close()
        self.driver.close()



app = Flask(__name__)
CORS(app)
# 在这里定义你想要识别的实体类型
schema = [{"人名": "身份"},{'人的代称':"隶属"},{'政策':"发布单位"},{'政策':"针对群体"},{'法规条例':"发布单位"},{'法规条例':"针对群体"},{'事件工程项目':"发布单位"},{'事件工程项目':"针对群体"},{'会议':"发言人"},{'会议':"发布内容"},{'会议':"开会地点"},
          '政府机构', '省份','城市地点','组织机构企业','新闻杂志融媒体','国家']

# 设定抽取目标和定制化模型权重路径
my_ie = Taskflow("information_extraction", schema=schema, task_path='../uie-model/checkpoint/model_best4000')

@app.route('/', methods=['POST'])
def process_text():
    text = request.json['text']
    results = my_ie(text)
    print(text)
    nodes = []
    links = []
    node_ids = set()  # 用于存储节点ID，以检查是否有重复的节点
    link_sources_targets = set()  # 用于存储链接的source-target组合，以检查是否有重复的链接
    nodes_dict = {}
    for result in results:
        for key, values in result.items():
            for value in values:
                node_id = value['start']
                if node_id not in node_ids:  # 检查该节点ID是否已经存在
                    node = {
                        'id': node_id,
                        'label': key,
                        'text': value['text'],
                        'start': value['start'],
                        'end': value['end'],
                        'probability': float(value['probability']),
                        'hasRelation': 1 if 'relations' in value else 0
                    }
                    nodes.append(node)
                    nodes_dict[node['id']] = node
                    node_ids.add(node_id)  # 将新节点ID添加到集合中

    for result in results:
        for key, values in result.items():
            for value in values:
                if 'relations' in value:
                    for relation_type, related_entities in value['relations'].items():
                        for related_entity in related_entities:
                            # 创建一个source-target组合字符串来检查重复的链接
                            source_target_str = f"{value['start']}-{related_entity['start']}"
                            if source_target_str not in link_sources_targets:  # 检查该链接是否已经存在
                                links.append({
                                    'source': value['start'],
                                    'target': related_entity['start'],
                                    'sourceText': value['text'],
                                    'sourceLabel': key,
                                    'targetText': related_entity['text'],
                                    'targetLabel': nodes_dict[related_entity['start']]['label'],
                                    'relation': relation_type
                                })
                                link_sources_targets.add(source_target_str)  # 将新链接的source-target组合添加到集合中

    nodes = sorted(nodes, key=lambda x: x['start'])
    links = sorted(links, key=lambda x: x['source'])
    print(nodes)
    print(links)
    # example = Example()
    # bolt_url = "bolt://124.126.103.210:4001"
    # username = "SYSDBA"
    # password = "SYSDBA"
    # example.connect(bolt_url, (username, password))
    # example.create_graph(nodes, links)
    # example.disconnect()

    return jsonify({
        'nodes': nodes,
        'links': links,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=888)
