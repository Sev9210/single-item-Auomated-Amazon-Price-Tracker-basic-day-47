import requests
import re
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
load_dotenv()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Device-Memory": "8",
}
url = 'https://www.amazon.com/COOFANDY-Casual-Shirts-Button-Summer/dp/B0BV241H3F/ref=zg_bs_g_121177981011_d_sccl_1/147-1172022-6466413?th=1&psc=1'

response = requests.get(url=url, headers=headers)
results = response.text

soup = BeautifulSoup(results, 'html.parser')

product = soup.find(id='productTitle').getText().strip()
price = soup.find(class_='a-price-whole').getText().strip().replace(',', '')
original_price = soup.select_one(
    '.basisPrice span[aria-hidden=true]').getText().replace('PHP', '').replace(',', '')
discount = int(soup.find(
    class_='apex-savings-container').getText().strip().replace('-', '').replace('%', ''))


def mail():

    gmail = os.getenv('GMAIL')
    secret = os.getenv('SECRET')
    gmail_reciever = os.getenv('RECIEVER')

    msg = EmailMessage()
    msg['Subject'] = 'Currnet Price of item'
    msg['From'] = gmail
    msg['To'] = gmail_reciever

    scraped_body = f'Product name: {product}\nPrice: Php {price}\n Original Price: Php {original_price}\nDiscount: -{discount}%\nLink: {url}'
    msg.set_content(scraped_body)

    try:
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=gmail, password=secret)
            connection.send_message(msg)
            print('message sent succesfully!')
    except Exception as e:
        print(f'Error {e}')


def send_mail():
    buying_discount = 30  # 30%(percent)
    if discount <= buying_discount:
        mail()


send_mail()
