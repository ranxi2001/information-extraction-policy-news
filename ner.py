#coding=utf-8
from pprint import pprint
from paddlenlp import Taskflow
# 在这里定义你想要识别的实体类型
schema = ['政策', '政府机构', '省份','城市地点','人名','人的代称','事件工程项目','会议','法规条例','组织机构企业','新闻杂志融媒体','国家']
# 设定抽取目标和定制化模型权重路径,删除task_path则下载使用UIE公开默认模型，默认模型下载后保存在paddlenlp仓库而不是本项目中，所以无法指定路径。
my_ie = Taskflow("information_extraction", schema=schema, task_path='uie-model/checkpoint/model_best4000')
# 获取信息抽取的结果
pprint(my_ie("新华社记者燕雁摄3月22日至25日上午，海南省长苏树林,省人大常委会主任蒲庆洪在海口考察。"))

