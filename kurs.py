import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule
import time
import psycopg2

def pars_tabl():

    def pars():
        r=requests.get("https://www.nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut")
        s=r.text

        soup = BeautifulSoup(s, 'html.parser')

        date=soup.find(class_="title-section")
        print(date.text.strip(), usd)

        usd=soup.find("td", string="USD / KZT").find_next_sibling().text

        global usd_title
        global usd_date
        global usd_cur
        usd_title = date.text.strip()[:-15]
        usd_date = date.text.strip()[39:]
        usd_cur=usd

    def tabl():
        connection = psycopg2.connect(
            dbname="kurs",
            user="postgres",
            password="Cgfkmybr36",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO kurs(Title, Data, ex_rate)
        VALUES(%s,%s,%s)
        """

        data = (usd_title,usd_date,usd)
        cursor.execute(insert_query,data)
        connection.commit()
        cursor.close()
        connection.close()

schedule.every().day.at("15:14").do(pars_tabl)

while True:
    schedule.run_pending()
    time.sleep(30)
