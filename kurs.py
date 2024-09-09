import requests
from bs4 import BeautifulSoup
import schedule
import time
import psycopg2

url = "https://www.nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut"
bd = {
    "dbname": "courses",
    "user": "postgres",
    "password": "Cgfkmybr36",
    "host": "localhost",
    "port": "5432"
}
def pars():
    try:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            date = soup.find(class_="title-section").text.strip()
            usd = soup.find("td", string="USD / KZT").find_next_sibling().text.strip()

            usd_title = date[:-15]
            usd_date = date[39:]
            usd_cur = usd

            return usd_title, usd_date, usd_cur
        else:
            print("Данные с сайта получить не удалось.")
            return None
    except Exception as e:
        print(f"Ошибка при парсинге данных: {e}")
        return None

def tabl():
    try:
        connection = psycopg2.connect(**bd)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id BIGSERIAL PRIMARY KEY,
                title VARCHAR(75),
                dt VARCHAR(15),
                currency VARCHAR(15)
            );
        """)
        connection.commit()
        print("Таблица создана или уже существует.")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def ins_data(title, date, currency):
    try:
        connection = psycopg2.connect(**bd)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO courses (title, dt, currency)
            VALUES (%s, %s, %s);
        """, (title, date, currency))
        connection.commit()
        print("Данные успешно сохранены в базу данных.")
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def job():
    tabl()
    data = pars()
    if data:
        ins_data(*data)

schedule.every().day.at("00:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(30)
