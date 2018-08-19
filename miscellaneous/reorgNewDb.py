import csv
import re
import pymysql
import traceback


conn = pymysql.connect(
        host="",
        db="tissue",
        user="translator", 
        password="",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
        )

with open('new_db.csv', 'r') as f2:
    csvReader = csv.reader(f2)
    cursor = conn.cursor()
    for line in csvReader:
        query = """INSERT INTO sejongUnitDic
                       (cnt, word, category, length)
                   VALUES
                       (%s, %s, %s, %s)
                """

        try:
            print(line)
            cursor.execute(query, (int(line[0]), line[1], line[2], int(line[3]), ))
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()
