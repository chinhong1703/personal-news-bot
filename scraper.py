import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.parser import parse

def scraperAP(keywords):
  url = 'https://www.androidpolice.com/'
  # get response and parse into bs
  resp = requests.get(url)
  soup = BeautifulSoup(resp.text,'html.parser')
  
  # find all header class: post-header for all posts
  posts = soup.find_all('header', attrs={'class':'post-header'})

  postDB = []
  
  for post in posts:
    ### find all h2 tags for title of article
    h2_title = post.find('h2')
    
    ### find all a tag within h2 for url to article
    post_link = h2_title.find('a')
    
    
    ### find all time tags time class="timeago-hover" for date of article published
    post_time = post.find('time', attrs={'class':'timeago-hover'})
    
    #print(h2_title.text)
    #print(post_link['href'])
    #print(post_time.text)
    #print('--------------')

    # check if post is from today and does it have the keywords desired and add it to postDB
    x = (datetime.today() + timedelta(hours=-7)).date()
    y = parse(post_time.text).date()
    if x == y and any(word in h2_title.text.lower() for word in keywords):
      postDB.append({'title':h2_title.text, 'date':post_time.text, 'link':post_link['href']})
   
  return postDB

