from db import last_date, view_category_expanses
import datetime
import sqlite3
message = ")5000 Заработок на фрилансе"
if message[0] == "+" or message[0] == "-":
    try:
        if isinstance(int(str(str(message).split(" ", maxsplit=1)[0])[1:]), int):
            print("Okey")
    except ValueError:
        pass
else:
    print("Are u gay?")
