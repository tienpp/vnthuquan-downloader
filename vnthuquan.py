#-*- encoding: utf-8 -*-
import httplib
import re
from pyquery import PyQuery as pq
import unicodedata
import sys
def fetch(url):
	headers = {'Cookie':'ASP.NET_SessionId=xx'}
	conn = httplib.HTTPConnection("vnthuquan.net")
	conn.request("GET", url, "", headers)
	res = conn.getresponse()
	print res.status, res.reason
	data = res.read()
	conn.close()
	chap_titles = re.findall(r'class="normal8">(.+?)</a>', data)
	len_story = len(chap_titles)
	chap_descript = re.findall(r'title="(.+?)"><div', data)
	tuaid = re.findall(r'thong_so\+="(\d+?)"', data)[0]
	d = pq(data)
	title = d('title').text()
	f = open(re.sub('[^A-Za-z0-9 \-,]+', '', unicodedata.normalize('NFKD', title).encode('ascii','ignore')) + '.html', 'w')
	if len_story:
		f.write('<body><table style="width:100%">')
		n = 0
		for x,y in zip(chap_titles,chap_descript):
			#x = x.html()
			f.write('<tr><td><a href="#phan' + str(n) + '">'+ x + ' - '  + y + '</a></td></tr>')
			n += 1
		f.write('</table>')
	else:
		# if not ch:
		# 	#truyen co 1 chap
		# 	ch = re.findall(r'<acronym title=" "><li  onClick="noidung1(\w*)', data)
		len_story = 1
	n = 0
	for ch_id in xrange(len_story):
		link = '/truyen/chuonghoi_moi.aspx?&rand=415.9540610185356'
		ch_link = 'tuaid=' + tuaid + '&chuongid=' + str(ch_id+1)
		headers = {'Cookie':'ASP.NET_SessionId=xx', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
		conn = httplib.HTTPConnection("vnthuquan.net")
		conn.request("POST", link, ch_link, headers)
		res = conn.getresponse()
		print res.status, res.reason
		data = res.read()
		conn.close()
		data = data.split('--!!tach_noi_dung!!--')[1:]
		x = 'class="tieude0anh" id="phan' + str(n) + '"'
		f.write(data[0].replace('class="tieude0anh"', x) + data[1])
		n += 1
	f.write('</body>')
	f.close()

	
link = sys.argv[1].replace('http://vnthuquan.net', '')
fetch(link)