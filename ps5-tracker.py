from twilio_auth_tokens import TWILIO_AUTH_TOKENS
from twilio.rest import Client
from bs4 import BeautifulSoup
import requests
import time

twilio_acc_sid = TWILIO_AUTH_TOKENS.get("twilio_sid")
twilio_auth = TWILIO_AUTH_TOKENS.get("twilio_token")
twilio_client = Client(twilio_acc_sid, twilio_auth)

audio_string = "One P S 5 found at "

def make_call():
    call = twilio_client.calls.create(
        # url='https://demo.twilio.com/docs/classic.mp3)',
        twiml='<Response><Say>P S 5 in stock now</Say></Response>',
        to='+18188253237',
        from_='+14046668055'
    )
    print(call.sid)


while True:
    time.sleep(3)

    URL = "https://www.nowinstock.net/videogaming/consoles/sonyps5/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    tracker_div = soup.find(id="trackerContent")

    for match in tracker_div.findAll('span'):
        match.unwrap()
    for match in tracker_div.findAll('img'):
        match.unwrap()
    for match in tracker_div.findAll(attrs={"href": "#"}):
        match.unwrap()

    trackerData = tracker_div.find("div", id="data").find_all("tr")

    for i in trackerData:
        # print(type(i))
        siteName = i.contents[1].string
        availability = i.contents[2].string

        # print(availability)

        if availability == "Out of Stock" or availability == "Not Tracking":
            # print(siteName)
            # print("continuing...")
            continue
        else:
            if siteName == None:
                print(siteName)
                continue
            if not siteName == 'Ebay : All Models' and not siteName == 'Name':
                print(siteName)
                make_call()