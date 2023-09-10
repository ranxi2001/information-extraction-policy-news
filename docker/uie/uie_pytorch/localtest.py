#coding=utf-8
from pprint import pprint
from uie_predictor import UIEPredictor
# 在这里定义你想要识别的实体类型
schema = [{"人名": "身份"},{'人的代称':"隶属"},{'政策':"发布单位"},{'政策':"针对群体"},{'法规条例':"发布单位"},{'法规条例':"针对群体"},{'事件工程项目':"发布单位"},{'事件工程项目':"针对群体"},{'会议':"发言人"},{'会议':"发布内容"},{'会议':"开会地点"},
          '政府机构', '省份','城市地点','组织机构企业','新闻杂志融媒体','国家']
# 设定抽取目标和定制化模型权重路径,删除task_path则下载使用UIE公开默认模型，默认模型下载后保存在paddlenlp仓库而不是本项目中，所以无法指定路径。
my_ie = UIEPredictor(model='uie-base',task_path='../checkpoint', schema=schema)

# 获取信息抽取的结果
# result = my_ie("新华社记者燕雁摄3月22日至25日，中共中央总书记、国家主席、中央军委主席习近平在福建考察。")

# 按照规则打印
# pprint(my_ie("新华社记者燕雁摄3月22日至25日，中共中央总书记、国家主席、中央军委主席习近平在福建考察。"))

pprint(my_ie("坚决贯彻系统观念，以本工作方案和“四保”企业（项目）疫情防控工作指南为统领，坚持“一行业一方案”，分行业（领域）制定疫情防控工作指南和白名单企业（项目）保障办法，形成“1+1+N”工作体系，细化政策举措，有针对性地推动各领域疫情防控和生产运营双线嵌合落到实处。河南省人民政府办公厅2022年5月25日河南省高效统筹疫情防控和经济社会发展工作方案为有力有序有效做好常态化疫情防控下全省经济运行工作，确保企业（项目）不发生聚集性疫情，确保重点企业、重点项目不停产不停工，最大限度减少疫情对经济社会发展的影响，制定本工作方案。1.常态常备制度。以县（市、区）为主体，指导白名单企业（项目）按照本行业（领域）疫情防控工作指南要求，从严从紧从细从实制定工作预案、完善防控设施、备足人力物资、优化生产流程，定期组织开展模拟演练和压力测试，确保平时能防、疫时有备。2.平急转换制度。"))