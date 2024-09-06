import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule
import time


def pars():
    r=requests.get("https://www.nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut")
    s=r.text

    soup = BeautifulSoup(s, 'html.parser')

    date=soup.find(class_="title-section")
# print(date.text.strip())

    usd=soup.find("td", string="USD / KZT").find_next_sibling().text

    global usd_title
    global usd_date
    global usd_cur
    usd_title = date.text.strip()[:-15]
    usd_date = date.text.strip()[39:]
    usd_cur=usd

def tabl():
    db=sqlite3.connect("baza.db")
    c = db.cursor()

# c.execute("""CREATE TABLE dell(
#     title text,
#     chislo integer,
#     cur integer
#  )""")


    c.execute("INSERT INTO dell(title,chislo,cur)"
          "VALUES(?,?,?)",
          (usd_title,usd_date,usd)
          )

    db.commit()
    db.close()

schedule.every().monday.at("11:00").do(pars())
schedule.every().tuesday.at("11:00").do(pars())
schedule.every().wednesday.at("11:00").do(pars())
schedule.every().thursday.at("11:00").do(pars())
schedule.every().friday.at("11:00").do(pars())

schedule.every().monday.at("11:00:30").do(tabl())
schedule.every().tuesday.at("11:00:30").do(tabl())
schedule.every().wednesday.at("11:00:30").do(tabl())
schedule.every().thursday.at("11:00:30").do(tabl())
schedule.every().friday.at("11:00:30").do(tabl())

while True:
    schedule.run_pending()
    time.sleep(30)
