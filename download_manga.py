import os	# os operations
import sys	# basic system api.
import requests	# requesting webpages.
from bs4 import BeautifulSoup	# scraping 


# url for requesting the data.
url = 'https://www.mangapanda.com'


def select_manga():

	#To list the top trending manga from the website
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'lxml')
	tags=soup.findAll("a", {"class": "popularitemcaption"})
	name=[] #Contains names of all the listed manga
	link=[]	#Contains corresponding link extensions
	for tag in tags:
		name.append(''.join(tag.contents))
		link.append(tag['href'])

	#List them
	print("\n-----Most Popular Manga-----\n\n")
	for i,entry in enumerate(name):
		print(i+1,"-",entry)

	# choose which manga to download
	index = int(input("\n\nEnter your choice [1-%d]: "%(len(name))))
	manga=name[index-1]

	# for clearing the screen acc to your system platform(unix or windows).
	os.system('cls' if os.name == 'nt' else 'clear')
	

	# create the mangapanda url for the anime.
	mangaURL = url + link[index-1]

	return mangaURL,manga



if __name__ == '__main__':

	
	
	# for clearing the screen acc to your system platform(unix or windows).
	os.system('cls' if os.name == 'nt' else 'clear')

	#Fetch the manga url from a given list of manga
	mangaURL,manga=select_manga()

	# used to get the list of all the chapter names for the manga.
	page = requests.get(mangaURL)
	soup = BeautifulSoup(page.text, 'lxml')
	l = soup.find("table", {"id": "listing"}).find_all("td")
	title=[] #Stores the chapter names
	for idx,val in enumerate(l):
		if idx%2==0:
			title.append(val.text.strip("\n").replace("/",' '))

	# create the directory for the manga.
	try:
		os.mkdir(manga)
	except Exception as e:
		pass

	for i in range(len(title)):

		try:
			# create directory for individual each chapter
			os.mkdir(manga+"/"+title[i])

		except Exception as e:
			pass


		print("\nDownloading {} ".format(title[i]))

		#Find no of pages in each chapter
		foldername=mangaURL+"/%d"%int(i+1)
		page = requests.get(foldername)
		soup = BeautifulSoup(page.text, 'lxml')
		no_pages=int(soup.find("div", {"id": "selectpage"}).text[-2:])
		print(no_pages,"pages....\n")

		#Go to each page and download it
		for j in range(1,no_pages+1):
			
			#Request each page 
			page=requests.get(mangaURL+"/%d/%d"%(i+1,j))
			soup=BeautifulSoup(page.text,'lxml')
			img_URL=soup.find("img",{"id":"img"})['src']

			#Download the URL to the directory
			image=requests.get(img_URL).content
			filename=manga+"/"+title[i]+"/"+"{0:0=3d}".format(j)
			with open(filename,"wb") as f:
				f.write(image)




		
		


