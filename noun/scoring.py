import pymysql
import copy
import math

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

    def _calcFreq(self, candidate):
        """
        각 파트의 카운트를 넣어 기하평균을 낸다.
        """
        tot_mul = 1
        for item in candidate:
            tot_mul = tot_mul * (item['cnt'] if item['cnt'] != 0   else 1 )

        ret = math.pow(tot_mul, 1.0 / float( len(candidate) ) )
        return ret

    def _checkJunction(self, front_tail, back_head, option=0):
        """
        단일 연결에 대하여 통계를 내는 함수

        1) 연결부분 앞뒷말이 모두 있는 경우 -> 해당 카운트를 가중치로 사용
        2) 연결부분 중 뒷 말이 있는 경우 -> 뒷말에 해당하는 카운트를 합한 다음 평균 내어 가중치로 사용
        3) 연결부분 중 앞 말이 있는 경우 -> 앞말에 해당하는 카운트를 합한 다음 평균 내어 가중치로 사용
        3) 없으면 가중치 1
        """
        cursor = self.conn.cursor()
        query_twoside = """
            SELECT cnt, front_tail, back_head
            FROM junction_info
            WHERE front_tail = %s AND back_head = %s
        """
        cursor.execute(query_twoside, (front_tail, back_head, ))
        ret = cursor.fetchone()
        if ret is not None and len(ret) > 0:
            if option == 0:
                return True, {'freq': ret['cnt'], 'case': "{},{}".format(front_tail, back_head)}
            else:
                pass

        tot = 1
        query_back = """
            SELECT SUM(cnt)/count(cnt) as freq, back_head
            FROM junction_info
            WHERE back_head = %s
            GROUP BY back_head
        """
        cursor.execute(query_back, (back_head, ))
        ret = cursor.fetchone()
        if ret is not None and len(ret) > 0 and ret['freq'] > 0:
            if option == 0:
                return True, {'freq': ret['freq'], 'case': ",{}".format(back_head)}
            else:
                tot = ret['freq']

        query_front = """
            SELECT SUM(cnt)/count(cnt) as freq, front_tail
            FROM junction_info
            WHERE front_tail = %s
            GROUP BY back_head
        """
        cursor.execute(query_front, (front_tail, ))
        ret = cursor.fetchone()
        if ret is not None and len(ret) > 0 and ret['freq'] > 0:
            if option == 0:
                return True, {'freq': ret['freq'], 'case': "{},".format(front_tail)}
            else:
                tot = tot * ret['freq']
        
        # Whole else
        if option == 0:
            return False, {'freq': 1, 'case': ""}

        else:
            return True, {'freq': math.sqrt(tot), 'case': ""}

    def scoring(self, candidates, option=0):
        """
        후보들의 우선순위 산정 함수

        각각의 연결부위에서 가중치를 따 온다음 기하평균을 낸다.

        Option
          0: (a,b)의 Junction 정보를 우선 사용
          1: (a, )와 ( , b)의 정보의 기하평균으로 사용
          2: 사전 정보만 사용
        """
        ret = []
        for unit_cand in candidates:
            total_multipled = 1
            for idx, unit_word in enumerate(unit_cand):
                if idx == len(unit_cand) - 1:
                    break

                if option != 2:
                    front_tail = unit_word['word'][-1]
                    back_head = unit_cand[idx+1]['word'][0]
                    is_exist, unit_score = self._checkJunction(front_tail, back_head, option)
                    print(is_exist, unit_score)
                    total_multipled = total_multipled * unit_score['freq']

                    score1 = math.pow(total_multipled,  1. / float(len(unit_cand)))
                    score2 = self._calcFreq(unit_cand)
                    score = score1 / 2.0 + score2
                    print("Junction: {}, Cnt: {}, Overall: {}".format(score1, score2, score))

                else:
                    score = self._calcFreq(unit_cand)
                    print("Score: {}".format(score))

            unit_item = {"score": score, "candidate": unit_cand}
            print(unit_item)
            ret.append(unit_item)

        ret = sorted(ret, key=lambda word: word['score'], reverse=True)
        print("Final res")
        for item in ret[:5]:
            print(item)

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

    try:
        ret = candObj.scoring(testset, option=2)

        for item in ret:
            print(item)

    except:
        print("인터넷 연결을 확인해주세요!")
