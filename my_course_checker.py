#Jaspal Bainiwal
#Script to check DeAnza college in Cupertino, CA class availability
#class search url follows the following format
#"https://www.deanza.edu/schedule/listings.html?dept="+dept+"&t="+term

import bs4 as bsoup
import requests
import time
import api_keys as key

print("Welcome to course waitlist watcher")
dept = input("Enter department id: ").upper()
term = input("Enter quarter term: ").upper()
crn = input("Enter course number to watch: ")
class_open = False

def email_event(course, crn, prof):
  event = key.EVENT_NAME
  ifttt_key = key.KEY
  payload = {"value1":course,"value2":crn,"value3":prof}
  r = requests.post('https://maker.ifttt.com/trigger/' + event + '/with/key/' + ifttt_key, json=payload)
  print("Email sent")
  return

def class_checker():
  url = "https://www.deanza.edu/schedule/listings.html?dept="+dept+"&t="+term
  response = requests.get(url)
  soup = bsoup.BeautifulSoup(response.text, "html.parser")
  t_body = soup.find("tbody")
  tr = t_body.find_all("tr")

  for x in tr:
    td = x.find_all('td')
    if (td[0].get_text()) == crn:
      #if this is the correct course number
      if (td[3].get_text().upper()) == 'OPEN':
        course_name = td[4].find("a", href=True).get_text()
        prof_name = td[7].get_text()
        email_event(course_name, crn, prof_name)
        class_open = True
        return class_open

while class_open != True:
  class_open = class_checker()
  time.sleep(3600)
