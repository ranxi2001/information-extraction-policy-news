# 项目背景
> 2023年第十八届“挑战杯”全国大学生课外学术科技作品竞赛“揭榜挂帅”专项赛
>
> 推报学校名称： 浙江工商大学
>
> 参加竞榜的选题发榜单位： 中国软件与技术服务股份有限公司
>
> 参加竞榜的选题名称： 基于信创的学习迁移模型构建知识图谱
>
> 申报作品具体名称： 融智图谱——学习迁移模型构建知识图谱

# 使用说明

> 针对源代码的使用说明

## 项目架构

```
--揭榜挂帅
	--data-final：最终数据集（分为policy和news的train和test）格式为重新按照句子分段的txt
	--data-origin：原始提供的多模态数据
	--data-preprocess：转换多模态数据为txtline数据格式的脚本
		--other-to-txt：第一步：将各种数据格式文件转换为txt文件
		--txt-resegment：第二步：将所有的txt文件重新分句，使得每个段落（\n）不至于太长。
		--train-test-split：第三步：将所有txt文件分为训练集和测试集
	--data-preprocessed：多模态数据转化后的txt格式的数据集
		--new-news：包含从wps、pdf和docx转换的txt文件
		--new-policy：原本的txt文件，因为policy只有txt文件
	--uie-model：基于飞桨UIE模型的迁移微调信息抽取模型
		--checkpoint：模型微调后模型保存到的目录
			--model_best4000：最终提交的模型文件目录，包含12个模型文件
		--data：放置用于测试、模型微调训练的数据文件
			--doccano_ext.json：其中只用放置这个标注的数据集文件，其余文件通过tran.sh脚本生成
		--deploy：UIE模型部署到服务器的基础代码目录，不需要修改
		--train.sh：从本目录下的data数据集获取train.txt数据进行模型微调训练的脚本
		--tran.sh：将doccano_ext.json文件转换为train.txt、test.txt、name.txt、dev.txt
		--model_evaluation：测试全部类型的实体与关系的准确率和召回率的脚本
		--model_debug.sh：测试各个类型的实体和关系的精确率和召回率的脚本
		--其余py文件：模型训练与测试等代码不用修改
	--autoapi.py：在服务器上提供api，通过接口访问模型并返回预测结果的脚本
	--localtest.py：在本地对事先输入的文本进行预测并返回预测结果的脚本
```

## 模型微调（训练）

1. 准备好标注好的数据`doccano_ext.json`，放进uie-model目录下的data文件夹内
2. 运行`tran.sh`，就会将从doccano导出的标注数据转化为模型的输入数据和测试数据
3. 运行`train.sh`，就可以开始训练`uie-base`模型，训练结束后会保存模型到checkpoint目录下的model_best路径下

## 模型测试

### 整体模型性能测试

运行`model_evaluation.sh`，就可以开始测试整个模型的精确率，召回率了，本模型的F1score能够达到96%，满足题目要求。

![](https://cdn.jsdelivr.net/gh/ranxi2001/blog-imgs@main/img/all-test.jpg)

### 各类实体和关系性能测试

运行`model_debug.sh`，就可以开始测试整个模型的精确率，召回率了，

**实体识别**精确率、召回率、F1-Score均高于95%.

![](https://cdn.jsdelivr.net/gh/ranxi2001/blog-imgs@main/img/20230601223054.png)

**关系提取**准确率（指F1Score）仅有1/7个(政策的针对地区)低于95%，其余均高于95%

![](https://cdn.jsdelivr.net/gh/ranxi2001/blog-imgs@main/img/20230601223434.png)

## 参数调整

参数调整请看UIE模型的参数介绍文档：`./uie-model/README.md`

或者在线版：[PaddleNLP/README.md at develop · PaddlePaddle/PaddleNLP (github.com)](https://github.com/PaddlePaddle/PaddleNLP/blob/develop/model_zoo/uie/README.md#模型微调)