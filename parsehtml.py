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
	html_page = urllib2.urlopen(url)
	return BeautifulSoup(html_page)


def getCategory(bs4_content):
	# i=0
	for cat in bs4_content.findAll("a", attrs={"class":"f14"}):
		url_cat = url_cats + cat.get('href')
		#print cat.string, url_cats
		time.sleep(5)
		cat_content = getContent(url_cat)
		#print "cat_content len="+`len(cat_content)`
		getFood(cat.string, cat_content) #pass category name
		# if i==0:
			# break

def getFood(catstr, bs4_content):
	# i=0
	for allcontent in bs4_content.findAll("ul",attrs={"class":"l3"}):
		for food in allcontent.findAll("a", attrs={"target":"_blank"}):
			url_food_postfix = food.get('href').split("/")[1]
			url_food = url_cats + url_food_postfix
			#url_food = url_food.strip()
			#print food.string, url_food
			time.sleep(5)
			food_content = getContent(url_food)
			#print "food_content len="+`len(food_content)`
			getNutrition(catstr, food.string, food_content)
			#print url_food, url_food.__len__()
			# if i==0:
				# break


def getNutrition(catstr, foodstr, bs4_content):
	#Cat,Food,Calorie,Protein,Fat,Carbonhydrate,Fiber,Vitamin A,Carotene,....
	finalstring = catstr + ',' + foodstr
	#print "nutrition content len="+`bs4_content.__len__()`
	# print content.string
	for allcontent in bs4_content.findAll("table",attrs={"class":"bx"}):
		global k
		if k==0:
			title_string = u"类别,名称,"
			for title in allcontent.findAll("th"):
				title_string += "," + title.text.strip()
			k=k+1
			print title_string
		#finalstring+=allcontent.string
	# 	#print finalstring
		for nutrition in allcontent.findAll("td"):
			# k=k+1
			finalstring += ',' + nutrition.text.strip()
	print finalstring

#print all contents
getCategory(getContent(url_cats))
