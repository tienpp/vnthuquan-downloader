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
	ch = re.findall(r'chuonghoi.aspx\?tid=(\w*)\'\)"><a', data)
	d = pq(data.replace('toolbar text-toolbar', 'tocxxx'))
	title = d('title').text()
	c = d('table.tocxxx')
	f = open(re.sub('[^A-Za-z0-9 \-,]+', '', unicodedata.normalize('NFKD', title).encode('ascii','ignore')) + '.html', 'wb')
	if not ch:
		#truyen co 1 chap
		ch = re.findall(r'chuonghoi.aspx\?tid=(\w*)', data)
	else:
		f.write('<body><table style="width:100%">')
		n = 0
		for x in c('a.normal8').items():
			x = x.html()
			f.write('<tr><td><a href="#phan' + str(n) + '">'+ x.encode('utf-8') +'</a></td></tr>')
			n += 1
		f.write('</table>')
	n = 0
	for ch_link in ch:
		ch_link = '/truyen/chuonghoi.aspx?tid=' + ch_link
		print ch_link
		headers = {'Cookie':'ASP.NET_SessionId=xx'}
		conn = httplib.HTTPConnection("vnthuquan.net")
		conn.request("GET", ch_link, "", headers)
		res = conn.getresponse()
		print res.status, res.reason
		data = res.read()
		conn.close()
		data = data.split('--!!tach_noi_dung!!--')[1:]
		#print data
		x = 'table width="97%" id="phan' + str(n) + '"'
		f.write(data[0].replace('table width="97%"', x) + data[1])
		n += 1
	f.write('</body>')
	f.close()

	
link = sys.argv[1].replace('http://vnthuquan.net', '')
fetch(link)