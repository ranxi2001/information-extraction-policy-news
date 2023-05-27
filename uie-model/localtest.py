from pprint import pprint
from paddlenlp import Taskflow
# 在这里定义你想要识别的实体类型
# schema = ['人名','人的代称','会议','国家']
schema = [{"人名": "身份"},'人的代称']
# 设定抽取目标和定制化模型权重路径
my_ie = Taskflow("information_extraction", schema=schema, task_path='./checkpoint/model_best3800')
pprint(my_ie("座谈会上，中国，美国，民革中央主席万鄂湘"))