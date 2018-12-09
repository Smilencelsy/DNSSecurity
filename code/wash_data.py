# coding: utf-8

file1 = open('domain.txt', 'r')

file2 = open('new.txt', 'w')

well_known_sites = ['gov.cn', 'edu.cn', 'ac.cn', 'com.cn', 'org.cn', 'net.cn', 'mil.cn', 'qq.com', 'baidu.com', 'taobao.com', 'tmall.com', \
'alipay.com', 'aliyun.com', 'jd.com', 'sohu.com', 'sina.com', 'weibo.com', '163.com', '360.cn', 'sogou.com', 'soso.com', 'hao123.com', \
'iqiyi.com', 'youku.com', 'douban.com', 'zhihu.com', 'csdn.net', 'kugou.com', 'yy.com', 'douyu.com', 'weather.com', 'plasway.com', \
'1688.com', 'netease.com', 'irs01.com', 'imtmp.net', 'in-addr.arpa', 'apple.com', 'icloud.com', 'google.com', 'youtube.com', 'skype.net', \
'skype.com', 'wikipedia.org', 'amazon.com', 'xiaomi.com', 'vivo.com', 'oppo.com', 'gionee.com', 'qiniucdn.com', 'qiniudns.com']

i = 1

second_level_domain = ''
second_level_cname = ''

for line in file1.readlines():
	domain = line.split(',')[1].split('.')
	second_level_domain = domain[len(domain)-2] + '.' + domain[len(domain)-1]

	if line.split(',')[4] == 'CNAME':
		line = line.split(';')[0]
		cname = line.split(',')[5].split('.')
		second_level_cname = cname[len(cname)-2] + '.' + cname[len(cname)-1]

	if second_level_domain not in well_known_sites and second_level_cname not in well_known_sites:
		file2.write(line)

	print(i)
	i += 1
