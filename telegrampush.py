import json
import os
import requests
from time import sleep
import datetime

#Bot token is masked(X) for security
url = "https://api.telegram.org/botXXXXXXXXX:AAFfL24A9NPjE6m2iTKY0SQKbXqpcIi_-k4/sendMessage?chat_id=-100118783XXXX&text="
title = "----------India COVID-19 Counts----------"


def get_count():
    url = "https://api.covid19india.org/data.json"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    data = parsed["statewise"][0]
    delta = parsed["statewise"][0]["delta"]
    confirmed = data['confirmed']
    todays = delta["confirmed"]
    deaths = data['deaths']
    recovered = data['recovered']
    lastupdatedtime = data['lastupdatedtime']
    return(confirmed,todays,deaths,recovered,lastupdatedtime)

def update_count(confirmed):
    with open("/root/covid19/count.txt","w") as temp:
       temp.write(str(confirmed))
       temp.flush()
       os.fsync(temp.fileno())

with open("/root/covid19/count.txt","r") as temp:
   count=int(temp.read())
   print(type(count))
   confirmed,todays,deaths,recovered,lastupdatedtime = get_count()
   confirmed = int(confirmed)
   print(type(confirmed))
   if(count != confirmed):
      print("Count changed: "+str(confirmed))
      requests.get(url+title+"\n"+"Total confirmed cases: "+str(confirmed)+"\n"+"Today's cases: "+str(todays)+"\n"+"Deaths: "+deaths+"\n"+"Recovered: "+recovered+"\n"+"Last updated: "+lastupdatedtime)
      update_count(confirmed)
   else:
      print("Count not changed")
