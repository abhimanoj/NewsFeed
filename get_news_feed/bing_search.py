import requests, csv, io, os, sys, traceback
import lxml.html as lh
from get_news_feed.bing_utils import *
import re
import random
import urllib
import lxml.html
import bs4
import sys
import csv
from threading import Thread 


def bing_bot_two(page_size=11):

	terms = open("get_news_feed/terms.txt").read().splitlines()
	for term in terms:
		try:
			final_list = []
			print(term)  
			
			csv_file_name = ('get_news_feed/data/{}.csv').format(term.replace(' ','_'))
			
			clear_file(csv_file_name)


			k = 0 
			for i in range(1,int(page_size),10):
				print(i)
				filename = 'get_news_feed/bing_url.html'
				filename_url = 'get_news_feed/bing_url_content.html'
				#create or clear file...
				clear_file(filename)

				url = 'https://www.bing.com/search?q=contactus%3a+{}&first={}&FORM=PERE{}'.format(term,str(i),str(k))
				k = k + 1

				## OPEN FILE
				fetch_page(url,filename)
				with io.open(filename, encoding='utf-8') as page: 
					html = remove_tag('strong',page.read())
				tree = lh.fromstring(html)

				## EXTRACT LINKS
				profiles = tree.xpath('//*[@class="b_algo"]')
				html_out = ''
				for index, profile in enumerate(profiles):
				
					try: 
                        
						temp_dict = {}
						new_emails = []
						new_numbers = []
						data_url = profile.xpath(".//a[@*]/@href")
						data_title = remove_nonprintable(profile.xpath(".//a[@*]")[0].text).replace(',','')
						
						temp_dict['url'] = data_url[0]
						temp_dict['title'] = data_title 
					 

						clear_file(filename_url)
						fetch_page(data_url[0],filename_url)

						try:
							with io.open(filename_url, encoding='utf-8') as page: 
								html_out = remove_tag('strong',page.read())					 
							#html_out =  fetch_request(data_url[0])
						except:
							pass
							
						new_emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", html_out, re.I)
						new_numbers = re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", html_out, re.I)
							 
						temp_dict['email'] = new_emails
						temp_dict['phone'] = new_numbers
					
						final_list.append(temp_dict)


						with open(csv_file_name,'a') as result_file:
							writer = csv.writer(result_file, dialect='excel')
 
							for line in final_list:
								try:
									date_is = line['url'].encode('utf-8')
								except:
									date_is = ''
									pass

								try:
									subject_is = line['title'].encode('utf-8')
								except:
									subject_is = ''
									pass

								try:
									from_is = []
									t = 0
									for p in range(0,5):
										
										if len(line['email']) > p  and p < 5:
											from_is.append(line['email'][p])
										elif p<= 4:
											from_is.append(' ')
 
								except: 
									print('error')
									pass

								try:
									snippet_is = []
									for get_number in line['phone']: 
										if len(get_number) > 10:
											snippet_is.append(get_number)
								except: 
									print('error_5')
									pass

							line_data = [data_url[0],data_title]
 
							writer.writerow(line_data + from_is + snippet_is)	
						 
							final_list  = [] 
							line_data = []

					except:
						print("Exception in user code:")
						print('-'*60)
						traceback.print_exc(file=sys.stdout)
						print('-'*60)

		except:
			print("Exception in user code:")
			print('-'*60)
			traceback.print_exc(file=sys.stdout)
			print('-'*60)

HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'accept-encoding': 'gzip, deflate, sdch',
           'accept-language': 'en-US,en;q=0.8',
           'upgrade-insecure-requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
 

def fetch_request(url): 
	try: 
		fetch_url = requests.get(url, headers=HEADERS)
	except:

		try:
			with eventlet.Timeout(10):
				fetch_url = requests.get(url, headers=HEADERS)
		except:
			try:
				with eventlet.Timeout(10):
					fetch_url = requests.get(url, headers=HEADERS)
			except:
				fetch_url = ''
		
	return fetch_url



def clear_file(name):
    f = open(name, "w")
    f.truncate()
    f.close()
 
if __name__ == "__main__":
	paze_size_is = open("get_news_feed/page_size.txt").read() 
	bing_bot_two(paze_size_is)
