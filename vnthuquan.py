#-*- encoding: utf-8 -*-
import requests
import re
from pyquery import PyQuery as pq
import unicodedata
import sys

domain = 'http://vnthuquan.org'

def fetch(url):
	headers = {'Cookie':'ASP.NET_SessionId=xx'}
	res = requests.get(domain + url, headers=headers)
	print res.status_code, res.reason
	data = res.text
	chap_titles = re.findall(r'">(.+?)</acronym>', data)
	print len(chap_titles), chap_titles
	len_story = len(chap_titles)
	chap_descript = re.findall(r'<acronym title="(.+?)"><a', data)
	print len(chap_descript), chap_descript
	chap_links = re.findall(r'"><a href="(.+?)">', data)[:-2]
	print len(chap_links), chap_links
	d = pq(data)
	title = d('title').text()
	f = open(re.sub('[^A-Za-z0-9 \-,]+', '', unicodedata.normalize('NFKD', title).encode('ascii','ignore')) + '.html', 'wb')
	if len_story:
		f.write('<body><table style="width:100%">')
		n = 0
		for x,y in zip(chap_titles,chap_descript):
			#x = x.html()
			f.write('<tr><td><a href="#phan' + str(n) + '">'+ x[69:-4].encode('utf8') + ' - '  + y.encode('utf8') + '</a></td></tr>')
			n += 1
		f.write('</table>')
	else:
		# if not ch:
		# 	#truyen co 1 chap
		# 	ch = re.findall(r'<acronym title=" "><li  onClick="noidung1(\w*)', data)
		len_story = 1
	n = 0
	for ch_id in xrange(len_story):
		link = chap_links[ch_id].replace('truyen.aspx?tid=', 'http://vnthuquan.org/truyen/chuongtext.aspx?tid=') + '&rand=267.3781815'
		headers = {'Cookie':'ASP.NET_SessionId=xx', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
		res = requests.get( link, headers=headers)
		print res.status_code, res.reason
		data = res.text
		data = data.split('--!!tach_noi_dung!!--')[1:]
		x = 'p align="center" class="style26" id="phan' + str(n) + '"'
		f.write(data[0].replace('p align="center" class="style26"', x).encode('utf8') + data[1].encode('utf8'))
		n += 1
	f.write('</body>')
	f.close()

	
link = sys.argv[1].replace(domain, '')
fetch(link)
