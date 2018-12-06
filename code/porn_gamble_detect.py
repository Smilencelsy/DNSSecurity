import pickle
import numpy as np
import linecache
import model_training as mt

def readFile():
	with open('../source/word.pick','rb') as keyword_pick:
		word_idx = pickle.load(keyword_pick)

	#读取人工标记的训练数据word_x
	word_dict={}
	for index,word in enumerate(word_idx):
		word_dict[word] = index
    
	return word_dict,word_idx

def gene_feature(word_dict,word_idx,count):
	#将数据编码成特征向量
	#特征向量采用一维one-hot编码
	#其中0位表示字典中未出现的词
	train_x=np.zeros((count,len(word_idx)+1))
	train_y=np.zeros((count,3))
	#共269个训练数据
	for i in range(count):
    	#奇数行分词
    	#偶数行标签
    	#1:色情 2:赌博 0:正常
		x_line = 2*i+1
		y_line = 2*i+2
		label = linecache.getline('../source/word_x.txt',y_line)

		label=label.strip('\n')

		if label=='0':
			train_y[i][0]=1
		elif label=='1':
			train_y[i][1]=1
		elif label=='2':
			train_y[i][2]=1

		line = linecache.getline('../source/word_x.txt',x_line)
		word_list = line.split(',')
		for word in word_list:
			if word_dict.get(word)!=None:
				index = word_dict.get(word)
				train_x[i][index] = 1
			else :
				train_x[i][0] = 1

	#生成随机数据索引
	#打乱训练数据
	permutation = np.random.permutation(train_x.shape[0])
	train_data = train_x[permutation, :]
	train_targets = train_y[permutation]

	return train_data,train_targets

def predict_result(word_idx,word_dict,model,n):
	#统计测试文件行数
	filename = "../source/word_" + str(n) + ".txt"
	with open(filename) as f:
		count = len(f.readlines())
    
	#处理测试数据
	f = open('../source/label.txt','a')
	for i in range(1,count):
		if i%2000 == 0:
			process = float(i)/float(count)
			p = "%.2f%%" % (process * 100)
			print str(n) , ' ' ,p
		if i%2 ==0 :
			continue
		line = linecache.getline(filename,i)

		word_list = line.split(',')
		url = word_list[0]
		test = np.zeros((1,len(word_idx)+1))
		for word in word_list:
			if word_dict.get(word)!=None:
				index = word_dict.get(word)
				test[0][index] = 1
			else :
				test[0][0] = 1

		#计算模型结果
		predict = model.predict(test)
		label = np.argmax(predict)

		f.write(url+","+str(label)+'\n')
	f.close()

def result_count():
	with open('../source/label.txt') as f:
		result_list = f.readlines()
	w_f = open('../source/porn_or_gamble.txt','a')
	for line in result_list:
		line = line.strip('\n')
		l = line.split(',')
		if len(l) > 1:
			if int(l[1]) == 1 or int(l[1]) == 2:
				w_f.write(l[0] + "," + l[1] + "\n")

	f.close()

if __name__ == "__main__":
	word_dict,word_idx = readFile()
	with open("../source/word_x.txt") as f:
		count = len(f.readlines())
	train_data,train_targets = gene_feature(word_dict,word_idx,count/2)
	model = mt.build_model(train_data)
	model = mt.k_train_data(train_data,train_targets,model)
	for i in range(1,6):
		predict_result(word_idx,word_dict,model,i)
	#result_count()


      


