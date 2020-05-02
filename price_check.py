import requests
import win10toast
import time
from bs4 import BeautifulSoup


products = {"https://www.kabum.com.br/produto/102174/teclado-mecanico-gamer-cooler-master-rgb-switch-gateron-red-us-ck-530-gkgr1?gclid=Cj0KCQjwka_1BRCPARIsAMlUmErRDq01BtPxpG-bkWk3zOlQd7nYzeu4KhFJ8VAnZ94mEaps3YLs_EQaAuXvEALw_wcB" : 470, 
            "https://www.kabum.com.br/produto/92065/teclado-mecanico-gamer-hyperx-alloy-fps-pro-led-switch-cherry-mx-red-us-hx-kb4rd1-us-r2" : 470}
toaster = win10toast.ToastNotifier()


def telegram_bot_sendtext(bot_message):
    bot_token = '<BOT TOKEN HERE>'
    bot_chatID = '<YOUR ID HERE>'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def check_prices():
    while True:
        for site, price in products.items():
            r = requests.get(site)
            soup = BeautifulSoup(r.content, "html.parser", from_encoding='latin-1')
            actual_price = float(soup.findAll("meta", {"itemprop": "price"})[0].get("content"))
            product_name = soup.findAll("div", {"id": "titulo_det"})[0].get_text().strip()
            if actual_price < price:
                toaster.show_toast("Python", f"Promocao do {product_name} a {actual_price}")
                telegram_bot_sendtext(f"Promocao do {product_name} a {actual_price}")
                return None
        time.sleep(900)

check_prices()