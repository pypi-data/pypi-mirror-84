import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
import pylab

from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


class Datasets():
    def __init__(self, name):
        data_name = name
        if data_name=='digits':
            self.data_total=datasets.load_digits()
            print("手写数字数据集加载完毕")

        elif data_name=='iris':
            self.data_total=datasets.load_iris()
            print("鸢尾花数据集加载完毕")

        elif data_name=='breast_cancer':
            self.data_total=datasets.load_breast_cancer()
            print("乳腺癌数据集加载完毕")

        elif data_name=='diabetes':
            self.data_total=datasets.load_diabetes()
            print("糖尿病数据集加载完毕")

        elif data_name=='boston':
            self.data_total=datasets.load_boston()
            print("房价数据集加载完毕")

        elif data_name=='linnerud':
            self.data_total=datasets.load_linnerud()
            print("体能数据集加载完毕")

    # 对数据集进行划分
    def split(self,test_size, random_state):
        from sklearn.model_selection import train_test_split
        self.Xtrain,  self.Xtest,  self.Ytrain,  self.Ytest = train_test_split(self.data_total.data, self.data_total.target, test_size=test_size/100,
                                                        random_state=random_state);
        print("数据集划分结束，已分为" + str(random_state) + "类，其中测试集占" + str(test_size))

class model(Datasets):
    def __init__(name):
        super().__init__(self,name)
    #训练
    def train(self,name):
        print("开始"+str(name)+"训练")
        if name == svm:
            name=svm.SVC
        model = name(probability=True)
        self.model = model.fit(self.Xtrain, self.Ytrain)
        print("训练已结束")
    
    
    

# 模型保存
def save(model,name):
    import joblib
    filepath='../'+name
    joblib.dump(model, filepath);
    print("已保存模型为" + str(name))

# 模型加载
def load(name):
    import joblib
    filepath='../'+name
    self.model = joblib.load(filepath)
    print('模型' + name + "已成功加载")

def test():

# 模型测试
    def test(self):
        print("开始测试")
        print("测试结果为：" + str(self.model.score(self.Xtest, self.Ytest)))

    # 模型预测结果展示
    def predict1(self):
        Ypred = self.model.predict(self.Xtest)
        print("预测结果为" + str(Ypred))
        return

    # 模型预测——对单独图片结果展示
    def predict2(self,Xtest_n):
        B=self.model.predict_proba(Xtest_n.reshape(1, -1))
        print(B)
        print("预测结果为" + str(B))

'''
#赋值digits为加载的手写数字数据集
digits=Datasets('digits')
#打印digits的数据
print(digits.data)
#将digits以随机数种子2划分，其中测试集占比20%
digits.split(20,2)

#赋值model为digits以支持向量机算法训练所得模型
model=digits.train(svm)
#将model保存为xxx.pkl
save(model,xxxx.pkl)
#赋值model为加载的xxx.pkl模型
model=load(xxx.pkl)

#model开始测试
test(model,digits.Xtest,digits.Ytest)
#用模型xxx预测
predict1(model,digits.Xtest)

print(digits.Xtest[0])
digits.predict2(digits.Xtest[0])
'''