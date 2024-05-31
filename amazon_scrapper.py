from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
import csv
import datetime
from email.message import EmailMessage
import ssl

def send_mail():
    email_sender= "<Email>"
    email_password= "<Email Password>"
    email_reciever= "<Email>"

    subject = "The Headphones you want is below 149 AED! Now is your chance to buy!"
    body = "Ankit, This is the moment we have been waiting for. Now is your chance to pick up the headphones of your dreams. Don't mess it up! Link here: https://www.amazon.ae/Razer-BlackShark-V2-Gaming-Headset/dp/B089SSFV85/ref=sr_1_2?crid=26TVU1T2NZRXP&keywords=razer%2Bv2x&qid=1683379021&sprefix=razer%2Bv2%2Caps%2C248&sr=8-2&th=1"

    em= EmailMessage()
    em["From"]= email_sender
    em["To"]= email_reciever
    em["Subject"]= subject
    em.set_content(body)

    context= ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())

link = "https://www.amazon.ae/Razer-BlackShark-V2-Gaming-Headset/dp/B089SSFV85/ref=sr_1_2?crid=26TVU1T2NZRXP&keywords=razer%2Bv2x&qid=1683379021&sprefix=razer%2Bv2%2Caps%2C248&sr=8-2&th=1"

headers="<Personal-User-Agent>"

page = requests.get(link, headers=headers)

soup1 = BeautifulSoup(page.content, "html.parser")

soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

heading_content = soup2.find_all("span", class_="a-size-base a-text-bold")

data_content = soup2.find_all("span", class_="a-size-base po-break-word")

heading=[]

data=[]

c=0
for a in heading_content:
    c+=1
    if c in [3,4,5,6,7]:
        heading.append(a.text.strip())
heading.append("Price")
heading.append("Date")

for i in data_content:
    data.append(i.text.strip())

price=soup2.find("span", class_="a-offscreen").text.strip()
price=price[3:6]
data.append(price)
if(int(price) < 149):
    send_mail()
    
today = datetime.date.today()
today=str(today)
data.append(today)

with open('/Users/ankit/Documents/Projects/Aamzon_Scrapper/AmazonHeadphonePrice.csv', 'a', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)
