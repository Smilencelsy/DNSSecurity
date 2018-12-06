# encoding=utf-8
import sys
import pandas as pd
import numpy as np
import linecache
import re
import matplotlib.pyplot as plt
import time
#处理数据
def readfiles():
	with open('../source/all_list_results.txt') as f1:
		all_result = f1.readlines()
		all_result_dict = {}
		for line in all_result:
			line = line.strip('\n').split(',')
			if len(line) == 2:
				all_result_dict[line[0]] = int(line[1])

	with open('../source/bad_list_results.txt') as f2:
		bad_result = f2.readlines()
		bad_result_dict = {}
		for line in bad_result:
			line = line.strip('\n').split(',')
			if len(line) == 2:
				bad_result_dict[line[0]] = int(line[1])

	#提取白名单
	#df = pd.read_csv('../source/alexatop.csv')[:100000]
	#w_f = open('../source/white_list_results.txt','a')
	#tmp = list(set(all_result_dict.keys()).intersection(set(df['url'])))
	#white_result_list = []
	#for url in tmp:
	#	if all_result_dict[url] == 0:
	#		w_f.write(url + ',0' + '\n')
	#w_f.close()

	with open('../source/white_list_results.txt') as f3:
		white_result = f3.readlines()
		white_result_dict = {}
		for line in white_result:
			line = line.strip('\n').split(',')
			if len(line) == 2:
				white_result_dict[line[0]] = int(line[1])

	f1.close()
	f2.close()

	#从word_1.txt到word_5.txt中找出对应的url和labels
	w_f1 = open('../source/bad_list_labels.txt','a')
	w_f2 = open('../source/white_list_labels.txt','a')

	dict1 = {}
	dict2 = {}
	for i in range(1,6):
		filename = '../source/word_' + str(i) + '.txt'
		f = open(filename,'r')
		count = len(f.readlines())
		for j in range(count):
			if j%2 == 0 :
				continue
			else:
				line = linecache.getline(filename,j)
				word_list = line.split(',')
				url = word_list[0]
				if url in bad_result_dict.keys():
					dict1[url] = line
				if url in white_result_dict.keys():
					dict2[url] = line

	for e1 in dict1.keys():
		w_f1.write(dict1[e1])
	for e2 in dict2:
		w_f2.write(dict2[e2])

	w_f1.close()
	w_f2.close()

	domain_info_file = open('../source/domain300w.txt')
	w_f3 = open('../source/bad_list_dnsinfo.txt','a')
	w_f4 = open('../source/white_list_dnsinfo.txt','a')
	raw_result = domain_info_file.readlines()
	for line in raw_result:
		tmp_list = line.split(',')
		url = tmp_list[1]
		if url in bad_result_dict.keys():
			w_f3.write(line)
		if url in white_result_dict.keys():
			w_f4.write(line)

	domain_info_file.close()
	w_f3.close()
	w_f4.close()

#读取文件, 转换为字典形式
def trans_dict():
	#读取黑名单和白名单的域名信息文件
	with open('../source/bad_list_dnsinfo.txt','r') as f1:
		bad_lines = f1.readlines()
	with open('../source/white_list_dnsinfo.txt','r') as f2:
		white_lines = f2.readlines()

	#转换为以url为key的字典类型
	bad_dict = {}
	white_dict = {}
	for e in bad_lines:
		e = e.split(',')
		if e[1]:
			bad_dict[e[1]] = {'recur_server':e[0],'req_type':e[2],'TTL':int(e[3]),'resp_type':e[4],
			'resp_value':e[5].strip('\n').strip('\r')}

	for e in white_lines:
		e = e.split(',')
		if e[1]:
			white_dict[e[1]] = {'recur_server':e[0],'req_type':e[2],'TTL':int(e[3]),'resp_type':e[4],
			'resp_value':e[5].strip('\n').strip('\r')}	

	return bad_dict,white_dict

#词法特征
def lexical_count(url_list):
	feature_dict = {}
	for url in url_list:
		#统计url长度 不包含分隔符.
		feature_dict[url] = {'length':len(url.replace('.',''))}
		#统计分隔符.的出现次数
		feature_dict[url]['parse_count'] = url.count('.')
		#统计特殊字符个数
		feature_dict[url]['uniword_count'] = len(re.sub('\.|[a-zA-Z0-9]','',url))
		#统计数字占总长度的比例
		feature_dict[url]['digit_length'] = len(re.compile('\d').findall(url)) * 1.0 / feature_dict[url]['length']
		#分隔符内数字个数的最大值
		feature_dict[url]['max_digit_length'] = max([len(re.compile('\d').findall(sub_str)) for sub_str in url.split('.')])
		#分隔符间的最大长度
		feature_dict[url]['max_sub_length'] = max([len(sub_url) for sub_url in url.split('.')])
		#数字字母转换频率
		feature_dict[url]['digit_letter_count'] = len(re.compile(r'\d[a-zA-Z]').findall(re.sub('\.','',url)) + re.compile(r'[a-zA-Z]\d').findall(re.sub('\.','',url)))
	return feature_dict

#绘制特征图形
def lexical_draw(bad_feature_dict,white_feature_dict):
	feature_list = ['length','parse_count','uniword_count','max_digit_length','max_sub_length','digit_letter_count']
	feature_name = [u'域名长度',u'分隔符数量',u'特殊字符数量',u'分隔符内最大数字长度',u'分隔符间最大长度',u'数字字母转换频率']
	for i in range(len(feature_list)):
		x_line,y_line1,y_line2 = x_y_generate(bad_feature_dict,white_feature_dict,feature_list[i])
		plt.plot(x_line,y_line1,color='r',label='black_list')
		plt.plot(x_line,y_line2,color='g',label='white_list')
		plt.title(feature_list[i]) #标题
		plt.legend()
		plt.show()

	x_line = [0.1*x for x in range(11)]
	y_line1 = [0 for x in range(11)]
	y_line2 = [0 for x in range(11)]
	for key in bad_feature_dict.keys():
		y_line1[int(round(bad_feature_dict[key]['digit_length'] * 10))] += 1
	for key in white_feature_dict.keys():
		y_line2[int(round(white_feature_dict[key]['digit_length'] * 10))] += 1
	ave_length = ( len(bad_feature_dict) + len(white_feature_dict) ) * 1.0 /2
	y_line3 = [ (y*1.0/len(bad_feature_dict))*ave_length for y in y_line1]
	y_line4 = [ (y*1.0/len(white_feature_dict))*ave_length for y in y_line2]
	plt.plot(x_line,y_line3,color='r',label='black_list')
	plt.plot(x_line,y_line4,color='g',label='white_list')
	plt.title('digit_length_percent') #标题
	plt.legend()
	plt.show()

#生成横纵坐标
def x_y_generate(bad_feature_dict,white_feature_dict,feature_name):
	#计算最大长度
	max_length = 0
	for key in bad_feature_dict.keys():
		max_length = bad_feature_dict[key][feature_name] if bad_feature_dict[key][feature_name] > max_length else max_length
	for key in white_feature_dict.keys():
		max_length = white_feature_dict[key][feature_name] if white_feature_dict[key][feature_name] > max_length else max_length	

	#初始化x,y轴的值
	x_line = [x for x in range(max_length+1)]
	y_line1 = [0 for x in range(max_length+1)]
	y_line2 = [0 for x in range(max_length+1)]

	#生成y轴值
	for key in bad_feature_dict.keys():
		y_line1[int(bad_feature_dict[key][feature_name])] += 1
	for key in white_feature_dict.keys():
		y_line2[int(white_feature_dict[key][feature_name])] += 1

	#归一化
	ave_length = ( len(bad_feature_dict) + len(white_feature_dict) ) * 1.0 /2
	y_line3 = [ (y*1.0/len(bad_feature_dict))*ave_length for y in y_line1]
	y_line4 = [ (y*1.0/len(white_feature_dict))*ave_length for y in y_line2]

	return x_line,y_line3,y_line4


#网络特征
def inter_analysis(bad_dict,white_dict):
	pass

if __name__ == "__main__":
#	readfiles() 处理判别结果/黑名单/白名单数据
	bad_dict,white_dict = trans_dict()  #将文件数据转换为字典形式
	#统计分析域名的词法特征
	bad_dict_feature = lexical_count(bad_dict.keys())
	white_dict_feature = lexical_count(white_dict.keys())
	lexical_draw(bad_dict_feature,white_dict_feature)

	#统计分析域名的网络特征
	inter_analysis(bad_dict,white_dict)

