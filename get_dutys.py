# -*- coding: utf-8 -*-
import urllib2, string, time,codecs

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/31.0.1650.63 Chrome/31.0.1650.63 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def get_html(url):
	req = urllib2.Request(url,headers=hdr)
	try:
		response = urllib2.urlopen(req)
		source   = response.read()
	except urllib2.HTTPError, e:
		print "error opening site"
		source = e.fp.read()
	return source

def get_links(html):
	links=[]	
	pos = html.find("pharmacyshow.asp")
	while pos > 0:
		i = 0
		while html[pos+i] != "'":
			i = i + 1
		links.append(html[pos:pos+i])
		pos = html.find("pharmacyshow.asp",pos+i)
	return links

def duties (source):
	duty_list =[]
	pos = source.find("greenlink")
	while pos >0:
		i = 1
		j = 1
		while source[pos+i]!=">":
			i = i+1
		while source[pos+i+j]!="<":
			j = j +1
		duty_list.append(" ".join(source[pos+i+2:pos+i+j].split()))
		pos = source.find("greenlink",pos+i)
	return duty_list

def dutiesi(source):
	key_words=["Εφημερία","Φαρμακείο","Διεύθυνση","Περιοχή","Τηλέφωνο"]
	duty=[]
	for key in key_words:
		pos_tag = source.find(key)
		pos_tag_prime = source.find("<td",pos_tag+1)
		pos_tag_double = source.find("<td",pos_tag_prime+1)
		"""print source[pos_tag:pos_tag_double]"""
		while source[pos_tag_double] != '>':
			pos_tag_double=pos_tag_double+1
		i=1
		while source[pos_tag_double+i]!='<':
			i=i+1
		ins = source[pos_tag_double+2:pos_tag_double+i]
		duty.append(ins)
		pos_sc = source.find(":",pos_tag+i)
	
	return duty
			
			

base_url="http://www.fsa.gr/"
date =time.strftime("%d/%m/%Y")
area = "141"
request = base_url+"duties.asp?dateduty="+date+"&areaid="+area

source = get_html(request)

source=source.decode('iso-8859-7')

for y in get_links(source):
	pass	

for x in get_links(source):
	sc = get_html(base_url+x)
	sc = " ".join(sc.split())
	for k in dutiesi(sc):
		print k
	


txt = codecs.open("output.txt","w","utf-8")
txt.write(source)
txt.close

"""print request"""


