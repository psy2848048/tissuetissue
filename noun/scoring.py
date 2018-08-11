import pymysql
import copy

class Scoring(object):
    def __init__(self):
        self.conn = pymysql.connect(
                host="hotelchat.ce2zgalnsfar.ap-northeast-2.rds.amazonaws.com",
                db="tissue",
                user="translator", 
                password="noSecret01!",
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
                )

    def _checkJunction(self, front_tail, back_head):
        cursor = self.conn.cursor()
        query_twoside = """
            SELECT cnt, front_tail, back_head
            FROM junction_info
            WHERE front_tail = %s AND back_head = %s
        """
        cursor.execute(query_twoside, (front_tail, back_head, ))
        ret = cursor.fetchone()
        if ret is not None and len(ret) > 0:
            return True, {'freq': ret['cnt'], 'case': "{},{}".format(front_tail, back_head)}

        query_back = """
            SELECT SUM(cnt)/count(cnt) as freq, back_head
            FROM junction_info
            WHERE back_head = %s
            GROUP BY back_head
        """
        cursor.execute(query_back, (back_head, ))
        ret = cursor.fetchone()
        if ret['freq'] > 0:
            return True, {'freq': ret['freq'], 'case': ",{}".format(back_head)}

        query_front = """
            SELECT SUM(cnt)/count(cnt) as freq, front_tail
            FROM junction_info
            WHERE front_tail = %s
            GROUP BY back_head
        """
        cursor.execute(query_front, (front_tail, ))
        ret = cursor.fetchone()
        if ret['freq'] > 0:
            return True, {'freq': ret['freq'], 'case': "{},".format(front_tail)}
        
        # Whole else
        return False, {'freq': 1, 'case': ""}

    def scoring(self, candidates):
        ret = []
        for unit_cand in candidates:
            total_multipled = 1
            for idx, unit_word in enumerate(unit_cand):
                if idx == len(unit_cand) - 1:
                    break

                front_tail = unit_word['word'][-1]
                back_head = unit_cand[idx+1]['word'][0]
                is_exist, unit_score = self._checkJunction(front_tail, back_head)
                print(is_exist, unit_score)
                total_multipled = total_multipled * unit_score['freq']

            score = total_multipled ** ( 1 / len(unit_cand) )
            unit_item = {"score": score, "candidate": unit_cand}
            print(unit_item)
            ret.append(unit_item)

        ret = sorted(ret, key=lambda word: word['score'], reverse=True)
        return ret[:5]

if __name__ == "__main__":
    candObj = Scoring()
    testset = [
          [{'cnt': 0, 'word': '한국사물인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 0, 'word': '한국사물인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 0, 'word': '한국사물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 0, 'word': '진흥협회'}]
        , [{'cnt': 0, 'word': '한국사물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물인터넷진흥협회'}]
        , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 0, 'word': '진흥협회'}]
        , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 1779, 'word': '한국'}, {'cnt': 0, 'word': '사물인터넷진흥협회'}]
        , [{'cnt': 1779, 'word': '한국'}, {'cnt': 0, 'word': '사물인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 1779, 'word': '한국'}, {'cnt': 0, 'word': '사물인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 1779, 'word': '한국'}, {'cnt': 292, 'word': '사물'}, {'cnt': 0, 'word': '인터넷진흥협회'}]
        , [{'cnt': 1779, 'word': '한국'}, {'cnt': 292, 'word': '사물'}, {'cnt': 0, 'word': '인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 1779, 'word': '한국'}, {'cnt': 292, 'word': '사물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 0, 'word': '진흥협회'}]
        , [{'cnt': 1779, 'word': '한국'}, {'cnt': 292, 'word': '사물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물인터넷진흥협회'}]
        , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
        , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 0, 'word': '진흥협회'}]
        , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
        ]

    ret = candObj.scoring(testset)

    for item in ret:
        print(item)
