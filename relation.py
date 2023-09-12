#coding=utf-8
from pprint import pprint
from paddlenlp import Taskflow
# 在这里定义你想要识别的实体类型
schema = [{"人名": "身份"},{'人的代称':"隶属"},{'政策':"发布单位"},{'政策':"针对群体"},{'法规条例':"发布单位"},{'法规条例':"针对群体"},{'事件工程项目':"发布单位"},{'事件工程项目':"针对群体"},{'会议':"发言人"},{'会议':"发布内容"},{'会议':"开会地点"}]
# 设定抽取目标和定制化模型权重路径,删除task_path则下载使用UIE公开默认模型，默认模型下载后保存在paddlenlp仓库而不是本项目中，所以无法指定路径。
my_ie = Taskflow("information_extraction", schema=schema, task_path='uie-model/checkpoint/model_best4000')
# 获取信息抽取的结果
pprint(my_ie("新华社记者燕雁摄3月22日至25日上午，海南省长苏树林,省人大常委会主任蒲庆洪在海口考察。"))