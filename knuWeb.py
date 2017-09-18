from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as uReq
import os.path
import time, json, subprocess



class knuNews_Slack_Bridge:
	tempLink = []
	newLink = []
	tempLink_href = []
	newLink_href = []
	tempLink_title = []
	newLink_title = []
	target_url = ""
	updatedNews = ""
	updateHref = ""

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
				tempTitle = str(news.get('title'))
				tempHref = str(news.get('href'))
				self.tempLink_title.append(tempTitle)
				self.tempLink_href.append(tempHref)
				print(tempHref)
				print(tempTitle)
				

	def initialJsonUpdate(self):
		
		for numLink in range(0, len(self.tempLink)):
			time.sleep(5)
			f = open("temp.json", "w")
			f.write('''{
					"username" : "KNU_NEWS_FEED",
					"icon_emoji" : ":ghost:",
					"attachments" : [
					{
						"color":"danger",
						"fields" : [
						{
							"title":"''' + self.tempLink_title[numLink] + '''",
							"value": "'''+ target_url + self.tempLink_href[numLink] +'''",
							"short":false
						}
						]
					}
					]
				}''')

			command = """curl -X POST -H 'Content-type: application/json' --data @temp.json https://hooks.slack.com/services/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"""
			p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)	
			out, err = p.communicate()	



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
				self.updatedNews = self.newLink_title[i]
				self.updatedHref = self.target_url + self.newLink_href[i]
				return 1
		return 2

	def updateLinks(self):
		self.tempLink = self.newLink
		self.tempLink_title = self.newLink_title
		self.tempLink_href = self.newLink_href

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
				newTitle = str(new_news.get('title'))
				newHref = str(new_news.get('href'))
				self.newLink_title.append(newTitle)
				self.newLink_href.append(newHref)
				print(new_news)

	def export_json_updated(self):
		for numLink in range(0, len(self.tempLink)):
			time.sleep(5)
			f = open("temp.json", "w")
			f.write('''{
					"username" : "KNU_NEWS_FEED",
					"icon_emoji" : ":ghost:",
					"attachments" : [
					{
						"color":"danger",
						"fields" : [
						{
							"title":"''' + self.updatedNews + '''",
							"value": "'''+ self.updateHref +'''",
							"short":false
						}
						]
					}
					]
				}''')

			command = """curl -X POST -H 'Content-type: application/json' --data @temp.json https://hooks.slack.com/services/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"""
			p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)	
			out, err = p.communicate()	


	def testify(self):
		print(self.newLink)
		print(self.tempLink)
		print("test Finished")
			
	
if __name__ == "__main__":

	target_url = 'http://computer.knu.ac.kr/07_sub/01_sub.html'
	a = 2

	knuParser = knuNews_Slack_Bridge(target_url)
	knuParser.testify()	
	knuParser.initialJsonUpdate()

	while(1):
		knuParser.checkNewFeed()
		a = knuParser.compareNewFeeds()
		if a is 1:
			knuParser.updateLinks()
		time.sleep(1800)

