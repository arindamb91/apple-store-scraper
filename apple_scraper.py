import requests
import string
import time
from bs4 import BeautifulSoup
import pymysql

alphabets=list(string.ascii_uppercase)
alphabets=alphabets[:1]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
}
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='customprojects',charset='utf8mb4')
print("db connected")

def exractpages():
	# links={}
	# count=0
	sublinks=[]
	for i in alphabets:
		count=count+1
		sublinks=[]
		print(i)
		# r=requests.get("https://itunes.apple.com/us/genre/ios-games/id6014?mt=8&letter="+i,verify=False,headers=headers,timeout=30)
		time.sleep(3)
		for j in range(1,2):
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
	return sublinks

def extractappdetails(sublinks):



if __name__ == '__main__':
	sublinks=exractpages()
	extractappdetails(sublinks)




