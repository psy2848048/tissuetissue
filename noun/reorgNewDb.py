import csv
import re
import pymysql
import traceback


#with open('new_db.txt', 'r') as f:
#    with open('new_db.csv', 'w') as f2:
#        csvWriter = csv.writer(f2)
#
#        content = f.read()
#        content = content.split('\n')
#        for line in content:
#            find_obj = re.search(r'(.*?)/(.*?), ([0-9]+)', line)
#            if find_obj is None:
#                continue
#
#            word = find_obj.group(1)
#            category = find_obj.group(2)
#            cnt = int(find_obj.group(3))
#            length = len(word)
#
#            csvWriter.writerow([cnt, word, category, length])


conn = pymysql.connect(
        host="hotelchat.ce2zgalnsfar.ap-northeast-2.rds.amazonaws.com",
        db="tissue",
        user="translator", 
        password="noSecret01!",
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
