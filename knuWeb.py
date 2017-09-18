from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as uReq
import os.path
import time, json



class knuNews_Slack_Bridge:
	tempLink = []
	newLink = []
	target_url = ""

	def __init__(self, targetUrl):
		self.target_url = targetUrl
		 
		targetClient = uReq(target_url)
		targetPage_html = targetClient.read()
		targetClient.close()
		targetPage_soup = bsoup(targetPage_html, "html.parser")
		comp_news = targetPage_soup.findAll("div", {'id':'myContainer'});

		for list in comp_news:
			for news in list.findAll("a", title=True):
				self.tempLink.append(str(news))
				print(news)

	

	def compareNewFeeds(self):
		for i in range(0, len(self.newLink)):
			#time.sleep(1)
			print(self.newLink[i])
			print(self.tempLink[i])

			if self.newLink[i] == self.tempLink[i]:
				print("they are same")

			else:
				print("new Update")
				print(self.newLink[i])
				return 1
		return 2

	def updateLinks(self):
		self.tempLink = self.newLink

	def checkNewFeed(self):
	
		print("checking for new feeds")
			
		newClient = uReq(target_url)
		newPage_html = newClient.read()
		newClient.close()
		newPage_soup = bsoup(newPage_html, "html.parser")
		new_comp_news = newPage_soup.findAll("div", {"id":'myContainer'});

		for new_list in new_comp_news:
			for new_news in new_list.findAll("a", title=True):
				self.newLink.append(str(new_news))
				print(new_news)

	def testify(self):
		print(self.newLink)
		print(self.tempLink)
		print("test Finished")
			
		
if __name__ == "__main__":

	target_url = 'http://computer.knu.ac.kr/07_sub/01_sub.html'
	a = 2

	knuParser = knuNews_Slack_Bridge(target_url)
	knuParser.testify()	


	while(1):
		knuParser.checkNewFeed()
		a = knuParser.compareNewFeeds()
		if a is 1:
			knuParser.updateLinks()
		time.sleep(100)

