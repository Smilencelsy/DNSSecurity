# coding=utf-8

import requests
from bs4 import BeautifulSoup
import jieba
import sys

punctuation = set(u''':!),.:;?]}'"、。〉》」』】〕〗〞︰︱︳！），．：；？｜｝︴､～‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝﹙﹛﹝（｛“‘-—_…/%<>+ \n\t''')
stop_words = ['了', '的', '不', '之', '着', '与', '和', '无', '个', '也']

#获取网页源代码
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
        AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'
    }
    try:
    	html = requests.get('https://'+url, headers = headers, timeout = 5)
    except Exception as e:
    	try:
    		html = requests.get('http://'+url, headers = headers, timeout = 5)
    	except Exception as e:
    		return None
    return html.content

def main():
	i = 1

	domain_file = open(sys.argv[1], 'r')
	lines = domain_file.readlines()

	word_file = open(sys.argv[2], 'w', encoding = 'utf-8')

	for line in lines:
		record = line.split(',')
		html = get_html(record[1])

		#如果http和https无法访问，访问别名CNAME
		if html is None and record[4]=='CNAME':
			html = get_html(record[5])

		#如果别名无法访问，访问次级域名
		if html is None:
			domain = record[1].split('.')
			html = get_html(domain[len(domain)-2] + '.' + domain[len(domain)-1])

		if html is not None:
			has_word = False
			soup = BeautifulSoup(html, 'lxml')

			#遍历源代码标签树，对标签包含的文本内容分词
			'''q = []
			q.append(soup.html)
			while q:
				current = q.pop(0)
				if current.string != None:
					for word in jieba.cut(current.string):
						if word not in punctuation:
							file.write(word+' ')
					continue
				for child in current.children:
					q.append(child)'''

			is_first_a = True
			for a in soup.find_all(name='a'):
				if a.string == None:
					pass
				else:
					a.string = ''.join(a.string.split())
					if is_first_a:
						has_word = True
						word_file.write(record[1] + ',')
						is_first_a = False
					for word in jieba.cut(a.string):
						if word not in punctuation and word not in stop_words and word.isdigit()!=True:
							word_file.write(word+',')

			if has_word == True:
				word_file.write('\n\n')

		print('dealed' + str(i))
		i += 1

if __name__ == '__main__':
	main()
