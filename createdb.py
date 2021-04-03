import sqlite3

db = sqlite3.connect("finance.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS budget("
               "total INT,"
               "savings INT)")
db.commit()

cursor.execute("INSERT INTO budget VALUES(0, 0)")
db.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS transactions("
               "id INTEGER PRIMARY KEY, "
               "action TEXT, "
               "sum INT,"
               "category TEXT,"
               "datetime date);")
db.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS category("
               "codename varchar(255) primary key,"
               "name varchar(255),"
               "month_expanses INT, "
               "is_necessarily BOOL, "
               "aliases TEXT);")
db.commit()

categories = [("products", "Продукты", 0, True, "продукты, еда, хавчик, перекус"),
              ("transport", "Транспорт", 0, True, "транспорт"),
              ("living", "Аренда", 0, True, "общага, общежитие, аренда, квартира, комната"),
              ("taxi", "Такси", 0, False, "такси, такса"),
              ("cafe", "Кафе", 0, False, "кофе, чай, кафе, кофейня"),
              ("clothes", "Одежда", 0, False, "шмот, шмотки, одежда, тряпки"),
              ("other", "Другое", 0, False, "")]

cursor.executemany("INSERT INTO category VALUES(?, ?, ?, ?, ?)", categories)
db.commit()
