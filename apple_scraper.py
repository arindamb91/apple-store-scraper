import requests
import string
import time
from bs4 import BeautifulSoup
import pymysql
from lxml import html
import pandas as pd

alphabets=list(string.ascii_uppercase)
alphabets=alphabets[1:5]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
}
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='customprojects',charset='utf8mb4')
print("db connected")

def extractpages():
	# links={}
	count=0
	# sublinks=[]
	for i in alphabets:
		count=count+1
		sublinks=[]
		# print(i)
		# r=requests.get("https://itunes.apple.com/us/genre/ios-games/id6014?mt=8&letter="+i,verify=False,headers=headers,timeout=30)
		time.sleep(3)
		for j in range(1,138):

			try:
				response=requests.get("https://itunes.apple.com/us/genre/ios-games/id6014?mt=8&letter="+i+"&page="+str(j)+"#"+"page",verify=False,headers=headers,timeout=30)
				print(response.url)
				time.sleep(3)
				soup=BeautifulSoup(response.content,'lxml')
				links=soup.select("a[href*=https://itunes.apple.com/us/app]")
				for link in links:
					sublinks.append(link.get('href'))
			except Exception as e:
				print(e)
				break
	# print(sublinks)
		# links[count]=sublinks
# 	return sublinks


# def extractappdetails(sublinks):
		for link in sublinks:
			cur=conn.cursor()
			appname,appconame,appcowebsite=("" for i in range(3))
			appdetails={}
			result=[]
			try:		
				r=requests.get(link,verify=False,headers=headers,timeout=30)
			except Exception as e:
				print('error in request')
				continue
			time.sleep(2)
			tree = html.fromstring(r.content)
			appdetails['applink']=link
			try:
				appname=tree.xpath("//h1[@class='product-header__title product-header__title--app-header']/text()")
				appname=appname[0].strip()
				# print(appname)
				# appdetails['appname']=appname

			except Exception as e:
				appname='NULL'

			try:	
				appconame=tree.xpath("//h2[@class='product-header__identity product-header__identity--app-header product-header__identity--spaced']/a[@class='link']/text()")
				appconame=appconame[0]
				# print(appconame)
				# appdetails['appconame']=appconame
			except Exception as e:
				appconame='NULL'
			try:	
				appcowebsite=tree.xpath("//li[@class='inline-list__item']/a[@class='link icon icon-after icon-external']/@href")
				appcowebsite=appcowebsite[0]
				# print(appcowebsite)
				# appdetails['appcowebsite']=appcowebsite
			except Exception as e:
				appcowebsite='NULL'
			cur.execute('insert into apple_app_details(app_link,app_name,app_coname,app_cowebsite)values(%s,%s,%s,%s)',(link,appname,appconame,appcowebsite))
			conn.commit()
			cur.close()
			# print(appdetails)



if __name__ == '__main__':
	# sublinks=exractpages()
	# extractappdetails(sublinks)
	extractpages()
