import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import json
import copy
import random
import matplotlib.pyplot as plt
import tqdm

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
max_length1 = 50
max_length2 = 500
# 从文件加载
with open('X_data.json', 'r') as file:
    data = json.load(file)
data = data[:8000]
data_copy = copy.deepcopy(data)
data1 = []
for i in range(len(data_copy)):
    data1.append(data[i][0])
data2 = []
for i in range(len(data_copy)):
    # 对长度进行截断或填充
    data0 = copy.deepcopy(data[i][1])
    if len(data[i][1]) > max_length1:
        data0 = copy.deepcopy(data[i][1][:max_length1])  # 截断
    else:
        data0 += [0] * (max_length1 - len(data[i][1]))  # 填充
    data2.append(data0)
data3 = []
for i in range(len(data_copy)):
    data3.append(data[i][2])
data4 = []
for i in range(len(data_copy)):
    # 对长度进行截断或填充
    data10 = copy.deepcopy(data[i][3])
    if len(data[i][3]) > max_length1:
        data10 = copy.deepcopy(data[i][3][:max_length1])  # 截断
    else:
        data10 += [0] * (max_length1 - len(data[i][3]))  # 填充
    data4.append(data10)
data5 = []
for i in range(len(data_copy)):
    data5.append(data[i][4])
data6 = []
for i in range(len(data_copy)):
    # 对长度进行截断或填充
    data20 = copy.deepcopy(data[i][5])
    if len(data[i][5]) > max_length2:
        data20 = copy.deepcopy(data[i][5][:max_length2])  # 截断
    else:
        data20 += [0] * (max_length2 - len(data[i][5]))  # 填充
    data6.append(data20)
labels = [1] * len(data)

#---------------------构建负样本---------------------
data11 = 2*data1
data21 = 2*data2
data31 = 2*data3
data41 = 2*data4
data52 = copy.deepcopy(data5)
random.shuffle(data52)
for i in range(len(data52)):
    if data52[i] == data5[i]:
        data52[i] = [0]
data51 = data5 + data52
for i in range(len(data51)):
    if np.random.rand() < 0.2:
        data51[i] = [0]
data61 = 2*data6
labels1 = labels + [0] * len(data)

# 定义一个MLP模型类
class MLPModel(nn.Module):
    def __init__(self, max_seq1=2000, max_seq2=12000, max_seq3=20, embedding_size=64):
        super(MLPModel, self).__init__()
        self.fc1 = nn.Linear(50*embedding_size, 32)
        self.fc2 = nn.Linear(32, 1)
        self.fc3 = nn.Linear(embedding_size, 32)
        # self.fc4 = nn.Linear(16, 1)
        self.fc5 = nn.Linear(500*embedding_size, 32)
        # self.fc6 = nn.Linear(16, 1)
        self.sigmoid = nn.Sigmoid()
        self.embed1 = nn.Embedding(max_seq1, embedding_size)
        self.embed2 = nn.Embedding(max_seq2, embedding_size)
        self.embed3 = nn.Embedding(max_seq3, embedding_size)
        self.flatten = nn.Flatten()
        self.dropout = nn.Dropout()

    def forward(self, x1, x2, x3, x4, x5, x6):
        x1 = self.embed3(x1)
        x1 = self.flatten(x1)
        x1 = self.fc3(x1)
        x1 = self.dropout(x1)
        x1 = torch.relu(x1) + x1
        x1 = self.fc2(x1)

        x3 = self.embed3(x3)
        x3 = self.flatten(x3)
        x3 = self.fc3(x3)
        x3 = self.dropout(x3)
        x3 = torch.relu(x3) + x3
        x3 = self.fc2(x3)

        x5 = self.embed3(x5)
        x5 = self.flatten(x5)
        x5 = self.fc3(x5)
        x5 = self.dropout(x5)
        x5 = torch.relu(x5) + x5
        x5 = self.fc2(x5)

        x2 = self.embed1(x2)
        x2 = self.flatten(x2)
        x2 = self.fc1(x2)
        x2 = self.dropout(x2)
        x2 = torch.relu(x2)
        # x2 = self.fc2(x2)

        x4 = self.embed1(x4)
        x4 = self.flatten(x4)
        x4 = self.fc1(x4)
        x4 = self.dropout(x4)
        x4 = torch.relu(x4)
        # x4 = self.fc2(x4)

        x6 = self.embed2(x6)
        x6 = self.flatten(x6)
        x6 = self.fc5(x6)
        x6 = self.dropout(x6)
        x6 = torch.relu(x6)
        x6 = self.fc2(x6)

        x2_x4_x6 = x2 + x4 + x6
        x2_x4_x6 = self.fc2(x2_x4_x6)
        x2 = self.fc2(x2)
        x4 = self.fc2(x4)
        x = self.sigmoid(x1+x2+x3+x4+x5+x2_x4_x6+x6)
        return x

# 创建模型实例
model = MLPModel().to(device)

# 定义损失函数和优化器
criterion = nn.BCELoss()  # 二元交叉熵损失
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam优化器

# 训练模型
epochs = 20
batch_size = 256
n = len(data2)//batch_size
loss_data = []
if __name__ == "__main__":
    for epoch in range(epochs):
        # 将多个列表合并成一个元组列表
        combined_lists = list(zip(data11, data21, data31, data41, data51, data61, labels1))
        # 打乱元组列表
        random.shuffle(combined_lists)
        # 将打乱后的元组列表拆分回多个列表
        shuffled_list1, shuffled_list2, shuffled_list3, shuffled_list4, shuffled_list5, shuffled_list6, shuffled_labels= zip(*combined_lists)
        loss_all = 0
        for batch in range(n):
            start = batch*batch_size
            end = (batch+1)*batch_size
            data1_tensors = shuffled_list1[start:end]
            data1_tensors = torch.tensor(data1_tensors).to(device)
            data2_tensors = shuffled_list2[start:end]
            data2_tensors = torch.tensor(data2_tensors).to(device)
            data3_tensors = shuffled_list3[start:end]
            data3_tensors = torch.tensor(data3_tensors).to(device)
            data4_tensors = shuffled_list4[start:end]
            data4_tensors = torch.tensor(data4_tensors).to(device)
            data5_tensors = shuffled_list5[start:end]
            data5_tensors = torch.tensor(data5_tensors).to(device)
            data6_tensors = shuffled_list6[start:end]
            data6_tensors = torch.tensor(data6_tensors).to(device)
            labels_tensor = shuffled_labels[start:end]
            labels_tensor = torch.tensor(labels_tensor).view(-1, 1).to(device)
            optimizer.zero_grad()  # 梯度清零
            outputs = model(data1_tensors, data2_tensors, data3_tensors, data4_tensors, data5_tensors, data6_tensors)  # 前向传播
            loss = criterion(outputs, labels_tensor.float())  # 计算损失
            loss.backward()  # 反向传播
            optimizer.step()  # 更新参数
            loss_all += loss

        print(f'Epoch [{epoch+1}/{epochs}], Loss: {(loss_all/len(data2))*100:.4f}')
        loss_all = loss_all.detach().numpy()
        loss_data.append((loss_all/len(data2))*100)

    torch.save(model.state_dict(), 'my_model.pth')  # 保存模型参数
    # 创建 x 轴数据（epochs 或迭代次数）
    epochs = range(1, len(loss_data) + 1)

    # 绘制损失函数曲线
    plt.plot(epochs, loss_data, 'b', label='Loss')
    plt.title('Loss Over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

