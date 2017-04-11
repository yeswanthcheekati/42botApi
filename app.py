from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import simplejson as json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/hello', methods=['POST'])
def hello():
    res.headers
    return "hi"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    ramy = processRequest(req)
    res = json.dumps({
        "speech": req['id'],
        "displayText": ramy,
        "data": {
            "slack":{
                "text":ramy
            }
        },
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    })
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def get_job_listings():
    url = 'https://www.42hertz.com/careers/'
    page = urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    jobs = soup.find(None, {"class":"job_listings"})
    job_info = []
    for element in jobs.find_all('a'):
        location = element.find(None,{"class":'location'}).text
        location = location.replace('\n','')
        location = location.replace('\t','')
        temp = {
        'link': element['href'],
        'location' : location,
        'position' : element.h3.text,
        'type':element.li.text,
        'Posted':element.find(None,{'class':'date'}).text
        }
        job_info.append(temp)
    temp = ''
    for d in job_info:
        temp = temp + '\t'.join(d.values()) + '\n'
    return temp

def get_services():
    url = 'https://www.42hertz.com/services/'
    page = urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    services = soup.find_all(None,{'class':'heading-int uppercase '})
    service = []
    for element in services:
        service.append(element.text)
    temp = '\r\n'.join(service)
    return temp

def get_people():
    url = 'https://www.42hertz.com/about-us/'
    page = urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    names_pos = soup.find_all(None,{'style':'text-align: center;'})
    names = soup.find_all('strong')
    pos = soup.find_all('em')
    people = []
    for i in range(0,4):
        temp = {
        'name': names[i+1].text,
        'designation' : pos[i].text
        }
        people.append(temp)
    temp = ''
    for d in people:
        temp = temp + '\t'.join(d.values()) + '\n'
    return temp

def processRequest(req):
    if req["result"]["action"] == "get_job_listings":
        data = get_job_listings()
    if req["result"]["action"] == "get_people":
        data = get_people()
    if req["result"]["action"] == "get_service":
        data = get_services()
    return data

def makeWebhookResult(data):
    return {
        "speech": data,
        "displayText": data,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
