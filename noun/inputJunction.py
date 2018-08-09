import re
import pymysql
import traceback

conn = pymysql.connect(
        host="hotelchat.ce2zgalnsfar.ap-northeast-2.rds.amazonaws.com",
        db="tissue",
        user="translator", 
        password="noSecret01!",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
        )

query = """
    INSERT INTO junction_info
      (front_tail, back_head, cnt)
    VALUES
      (%s, %s, %s)
"""

with open('dict_segment_boundaries_freq.txt', 'r') as f:
    content = f.read().split('\n')
    cursor = conn.cursor()

    for line in content:
        find_obj = re.search(r'(.*?),(.*?)\s([0-9]+)', line)
        if find_obj is None:
            continue

        first_word = find_obj.group(1)
        second_word = find_obj.group(2)
        cnt = int(find_obj.group(3))
        print(first_word, second_word, cnt)

        try:
            cursor.execute(query, (first_word, second_word, cnt, ))
            conn.commit()

        except:
            traceback.print_exc()
            conn.rollback()
