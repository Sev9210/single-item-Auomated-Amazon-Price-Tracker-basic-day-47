import requests
import re
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
load_dotenv()


def scrape_data():
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

    title_tag = soup.select_one('div#titleSection span#productTitle')
    scraped_title = title_tag.getText()
    title = re.sub(r'\s+', ' ', scraped_title).strip()

    price_discount_tag = soup.select_one(
        'span.apex-savings-container')
    discount = price_discount_tag.getText()
    price_tag = soup.select_one('span.a-price-whole')
    price = price_tag.getText()

    item_dict = {'Product': title,
                 'Discount': discount,
                 'Price': price,
                 'Link': url}

    return item_dict


scrape_data()


def mail(product, discount, price, link):
    gmail = os.getenv('GMAIL')
    secret = os.getenv('SECRET')
    gmail_reciever = os.getenv('RECIEVER')

    msg = EmailMessage()
    msg['Subject'] = 'Currnet Price of item'
    msg['From'] = gmail
    msg['To'] = gmail_reciever

    scraped_body = f'Product name: {product}\nPrice: {price}\n note: this item is now below $100.00\nDiscount: {discount}\nLink: {link}'
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

    items = scrape_data()
    product = items['Product']
    discount = items['Discount']
    link = items['Link']
    price = float(items['Price'].replace(',', ''))

    if price < 1600:
        print(f'{product}\n{discount}\n{price}\n{link}')
        mail(product, discount, price, link)


send_mail()
