import pymysql
import pandas as pd
import pickle
import os.path


DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

conn = pymysql.connect(
    host="hotelchat.ce2zgalnsfar.ap-northeast-2.rds.amazonaws.com",
    db="tissue",
    user="translator", 
    password="noSecret01!",
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
    )

def updateData(table_name):
    cursor = conn.cursor()
    query = "SELECT * FROM {}".format(table_name)
    cursor.execute(query)
    ret = cursor.fetchall()
    df = pd.DataFrame(ret)
    
    unit_dic_path = os.path.join(DATAPATH, '{}.pickle'.format(table_name))
    with open(unit_dic_path, 'wb') as f:
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)

updateData("sejongUnitDic")
updateData("junction_info")
