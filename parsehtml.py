# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

#import requests
import time
import urllib2
import re


url_cats = "http://yingyang.911cha.com/"
# response = requests.get(url)
# page = str(BeautifulSoup(response.content))
k=0

def getContent(url):
	html_page = urllib2.urlopen(url).read()
	return BeautifulSoup(html_page)


def getCategory(bs4_content):
	for cat in bs4_content.findAll("a", attrs={"class":"f14"}):
		url_cat = url_cats + cat.get('href')
		time.sleep(10)
		cat_content = getContent(url_cat)
		getFood(cat.string, cat_content) #pass category name

def getFood(catstr, bs4_content):
	for allcontent in bs4_content.findAll("ul",attrs={"class":"l3"}):
		for food in allcontent.findAll("a", attrs={"target":"_blank"}):
			url_food_postfix = food.get('href').split("/")[1]
			url_food = url_cats + url_food_postfix
			food_content = getContent(url_food)
			getNutrition(catstr, food.string, food_content)


def getNutrition(catstr, foodstr, bs4_content):
	#######Cat,Food,Calorie,Protein,Fat,Carbonhydrate,Fiber,Vitamin A,Carotene,....
	finalstring = "\n" + catstr + ',' + foodstr
	for allcontent in bs4_content.findAll("table",attrs={"class":"bx"}):
		global k
		if k==0:
			title_string = u"类别,名称,"
			for title in allcontent.findAll("th"):
				title_string += "," + title.text.strip()
			k=k+1
			print title_string
			finalstring += title_string
		for nutrition in allcontent.findAll("td"):
			finalstring += "," + nutrition.text.strip()
	f = open('myfile.csv','a')
	f.write(finalstring.encode('utf-8'))

#print all contents
getCategory(getContent(url_cats))
