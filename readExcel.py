#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#----------------------------------------------------------------------------  
# import modules   
#----------------------------------------------------------------------------  
from multiprocessing import Pool
import xlrd,random,urllib,requests,urllib2,os,threading,thread
source_path = '/data/zhangmeng/0517.xlsx'
#source_path = '/Users/finup/Downloads/0517.xlsx'
target_path = '/data/zhangmeng/mp3/'
#target_path = '/Users/finup/Downloads/mp3/'
phone_server_url ='http://phone-server.hh.production/v1/callRequest/getRecordingInvokeUrlByPhone'
#phone_server_url = 'http://localhost:8888/v1/callRequest/getRecordingInvokeUrlByPhone'
thread_count = 15

# excel是mp3的地址
def readExcel():
	workbook = xlrd.open_workbook(source_path) 
	print workbook.sheet_names()  

	data_sheet = workbook.sheets()[0]
	
	print data_sheet.nrows;
	mp3_urls = []
	split_urls = []
	index = -1
	for x in range(data_sheet.nrows):
		cell_type = data_sheet.cell(x,0).ctype
		mp3_url = data_sheet.cell(x,0).value
		if(mp3_url.strip() != '' and len(mp3_url) > 0):
			mp3_urls.insert(x,mp3_url)
			# print '索引的值为：',x
			# print '取余的值为：' ,int(x)%index_count
			if(x != 0 and (int(x)%index_count) == 0):
				# print '大索引：',(int(x)/index_count)
				split_urls.insert(index+1,mp3_urls)
				mp3_urls = []
			if(x+1 == data_sheet.nrows):
				split_urls.insert(index+1,mp3_urls)
	return split_urls;

def readExcelPhoneNum(batchNum,batch_count): 
	workbook = xlrd.open_workbook(source_path) 

	data_sheet = workbook.sheets()[0]


	# print '多进程',batchNum,batch_count
	mp3_urls = []
	x = 0
	while x < batch_count:
		#print '电话号码为：',int(data_sheet.cell(batchNum*batch_count +x,0).value)
		phoneNum = int(data_sheet.cell(batchNum*batch_count +x,0).value)
		x = x +1
		if(phoneNum > 0):
			# print '电话号码为：',phoneNum,x
			phoneNumDict = {}
			# 获取录音url
			url = getURL(phoneNum)
			# print 'url',url
			# if(url.strip() != '' and len(url) > 0):
			phoneNumDict[phoneNum] = url
			mp3_urls.insert(x,phoneNumDict)
	# print 'mp3个数',mp3_urls
	
	return mp3_urls

def readPhoneExcel():
	workbook = xlrd.open_workbook(source_path) 
	print workbook.sheet_names()  

	data_sheet = workbook.sheets()[0]
	
	print data_sheet.nrows;
	
	
	index = -1

	batch_count = 0
	if(data_sheet.nrows % thread_count == 0):
		batch_count = data_sheet.nrows / thread_count
	else:
		batch_count = data_sheet.nrows / thread_count +1

	
	p = Pool()
	split_urls = []

	for i in range(thread_count):
		print '当前进程',i
		result = p.apply_async(readExcelPhoneNum, args=(i,batch_count,),callback=downloadURL)
		# split_urls.insert(i,result.get())
	p.close()
	p.join()
	# return split_urls


# 获取录音url
def getURL(phoneNum):

		url=phone_server_url+"?phoneNum="+str(phoneNum) + "&callType=outbound&createTime=2018-06-12"

		req = urllib2.Request(url)
		req.add_header('Content-Type','application/json')
		try:
			print phoneNum
			resp = urllib2.urlopen(req)
		except urllib2.HTTPError,error:
				print "访问报错",error
				sys.exit(1)
		response = resp.read()
		print response
		if(response.strip() != '' and len(response) > 0):
			return eval(response)['data']
		return ''


def downloadURL(urls):
	print '是你么'
	print 'downloadURL',urls
	for x in urls:
		# print x
		
		for key,value in x.items():
			splits = value.split(',')
			if(value.strip() != '' and len(value) > 0):
				for s in splits:
					print '下载url',s,target_path+str(key)+'.mp3'
					try:
						f = urllib.urlretrieve(s, target_path+str(key)+'.mp3')
						# f.close()
						print 'downloan is done'
					except:
						print "404: Couldn't download file"
		# data=f.read()
		

if __name__ == '__main__':
	#getURL('12312312')

	readPhoneExcel()

	# print '二维数组为：',len(split_urls)
	# p = Pool()
	# for x in split_urls:
	# 	print '一维数组为：' ,x
	# 	p.apply_async(downloadURL, args=(x,))
	# p.close()
	# p.join()

